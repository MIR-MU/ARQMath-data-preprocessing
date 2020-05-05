# -*- coding:utf-8 -*-

import gzip
from itertools import chain
import json
from multiprocessing import Pool

from arqmathcode.post_reader_record import DataReaderRecord
from tqdm import tqdm

from .configuration import ARQMATH_COLLECTION_INPUT_DATA_DIRNAME, ARQMATH_COLLECTION_POSTS_LATEX_FILENAME, POOL_NUM_WORKERS, POOL_CHUNKSIZE
from .common import arqmath_post_read_html5_worker as read_html5_worker, Text, Math


XML_READER = DataReaderRecord(ARQMATH_COLLECTION_INPUT_DATA_DIRNAME)


def read_posts(name, post_map):
    posts = (
        (post.post_id, post.body)
        for post
        in sorted(post_map.values(), key=lambda post: post.post_id)
    )
    with Pool(POOL_NUM_WORKERS) as pool:
        converted_posts = tqdm(
            pool.imap(read_html5_worker, posts, POOL_CHUNKSIZE),
            total=len(post_map),
            desc='Converting {}'.format(name)
        )
        for post_id, input_document in converted_posts:
            output_document = []
            for input_token in input_document:
                assert isinstance(input_token, (Text, tuple))
                if isinstance(input_token, Text):
                    output_token = str(input_token)
                else:
                    _, math_token = input_token
                    assert isinstance(math_token, Math)
                    output_token = str(math_token)
                output_document.append(output_token)
            yield (post_id, output_document)


def read_questions():
    return read_posts('questions', XML_READER.post_parser.map_questions)


def read_answers():
    return read_posts('answers', XML_READER.post_parser.map_just_answers)


if __name__ == '__main__':
    with gzip.open(ARQMATH_COLLECTION_POSTS_LATEX_FILENAME, 'wt') as f:
        print('{', file=f)
        for post_id, post in chain(read_questions(), read_answers()):
            print(
                '"{}": {},'.format(
                    post_id,
                    json.dumps(post),
                ),
                file=f,
            )
        print('}', file=f)
