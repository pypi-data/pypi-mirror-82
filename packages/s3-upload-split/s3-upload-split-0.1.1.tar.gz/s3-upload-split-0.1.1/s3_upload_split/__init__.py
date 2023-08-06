__version__ = '0.1.0'

import io
import os
import re
import csv
import json
import time
import boto3
import logging
import threading

from anypubsub import create_pubsub

logger = logging.getLogger(__name__)
RE_TZ = re.compile('\+00:00$')


def dict_to_str(record):
    memory_file = io.StringIO()
    csv_writer = csv.writer(memory_file)
    csv_writer.writerow(list(record.values()))
    memory_file.seek(0)
    return next(memory_file)


class SplitUploadS3:
    def __init__(self, bucket, key, regex, iterator):
        self.bucket = bucket
        self.key = key
        self.regex = regex
        self.iterator = iterator
        self._patterns = dict()
        self._s3 = boto3.client('s3')

    def handle_content(self):
        pubsub, channel = create_pubsub('memory'), "chan1"
        for idx, record in enumerate(self.iterator):
            pattern = self.regex.search(dict_to_str(record)).group(1)
            if pattern not in self._patterns:
                logger.debug("Adding thread for pattern %s", pattern)
                json_output = os.path.join(self.key, f"data-{pattern}.json")
                uploading_thread = thread(self._s3, pubsub, channel, pattern, self.bucket, json_output)
                self._patterns[pattern] = 1
                uploading_thread.start()
            pubsub.publish(channel, (pattern, record))
        logger.info("Main thread has published all data, %d records, coming from the database", idx+1)
        while any([subscriber.messages.qsize() for subscriber in pubsub.subscribers[channel]]):
            logger.debug(f"Waiting as there are still messages that have not been read by subscribers...")
            time.sleep(10)
        logger.debug("Main thread finished, sending message to all subscribers that there is no more data")
        pubsub.publish(channel, (None, None))


def next_valid_data(iterable, matching_pattern, done=False):
    if done:
        raise StopIteration
    while True:
        pattern, data = next(iterable)
        if (data, pattern) == (None,)*2:
            raise StopIteration
        if pattern == matching_pattern:
            return data


def handle_value(value):
    return value if value is None or type(value) in [str, int] else RE_TZ.sub('', str(value))


def stringify(data):
    return {key:handle_value(value) for key, value in data.items()}


def jsonize(dictionary):
    return json.dumps(stringify(dictionary))


class thread(threading.Thread):
    def __init__(self, s3, pubsub, channel, pattern, bucket, filename):
        threading.Thread.__init__(self)
        self.s3 = s3
        self.subscriber = pubsub.subscribe(channel)
        self.pattern = pattern
        self.bucket = bucket
        self.filename = filename

    def iterable_to_stream(self, buffer_size=io.DEFAULT_BUFFER_SIZE):
        class IterStream(io.RawIOBase):
            def __init__(self, subscriber, pattern):
                self.leftover = None
                self.subscriber = subscriber
                self.pattern = pattern
                self.done = False

            def readable(self):
                return True

            def next_chunk(self):
                return jsonize(dict(next_valid_data(self.subscriber, self.pattern, self.done).items())) + "\n"

            def readinto(self, b):
                try:
                    l = len(b)  # We're supposed to return at most this much
                    chunk = self.leftover or self.next_chunk().encode()
                    output, self.leftover = chunk[:l], chunk[l:]
                    b[:len(output)] = output
                    return len(output)
                except StopIteration:
                    self.done = True
                    return 0  # indicate EOF

        return io.BufferedReader(IterStream(self.subscriber, self.pattern), buffer_size=buffer_size)

    def run(self):
        self.s3.upload_fileobj(self.iterable_to_stream(), self.bucket, self.filename)
