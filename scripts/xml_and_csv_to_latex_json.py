# -*- coding:utf-8 -*-

import gzip
from itertools import chain
import json
from multiprocessing import Pool
import sys

from arqmathcode.post_reader_record import DataReaderRecord
from arqmathcode.topic_file_reader import TopicReader
from tqdm import tqdm

from .configuration import ARQMATH_COLLECTION_INPUT_DATA_DIRNAME, ARQMATH_COLLECTION_POSTS_LATEX_FILENAME, POOL_NUM_WORKERS, POOL_CHUNKSIZE, ARQMATH_TASK1_TEST_INPUT_POSTS_FILENAME, ARQMATH_TASK1_TEST_POSTS_LATEX_FILENAME
from .common import arqmath_post_read_html5_worker as read_html5_worker, Text, Math


assert sys.argv[1] in ('collection', 'task1-topics')
if sys.argv[1] == 'collection':
    ARQMATH_POSTS_LATEX_FILENAME = ARQMATH_COLLECTION_POSTS_LATEX_FILENAME
    XML_READER = DataReaderRecord(ARQMATH_COLLECTION_INPUT_DATA_DIRNAME)
elif sys.argv[1] == 'task1-topics':
    ARQMATH_POSTS_LATEX_FILENAME = ARQMATH_TASK1_TEST_POSTS_LATEX_FILENAME
    XML_READER = TopicReader(ARQMATH_TASK1_TEST_INPUT_POSTS_FILENAME)


def read_posts(name, post_map, posts_are_topics):
    if posts_are_topics:
        posts = (
            (
                post.topic_id,
                '<Title>{}</Title><Question>{}</Question><Tags>{}</Tags>'.format(post.title, post.question, ' '.join(post.lst_tags)),
            )
            for post in sorted(post_map.values(), key=lambda post: post.topic_id)
        )
    else:
        posts = (
            (post.post_id, post.body)
            for post in sorted(post_map.values(), key=lambda post: post.post_id)
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
    return read_posts('questions', XML_READER.post_parser.map_questions, False)


def read_answers():
    return read_posts('answers', XML_READER.post_parser.map_just_answers, False)


def read_topics():
    return read_posts('topics', XML_READER._TopicReader__map_topics, True)


if __name__ == '__main__':
    with gzip.open(ARQMATH_POSTS_LATEX_FILENAME, 'wt') as f:
        print('{', file=f)
        if sys.argv[1] == 'collection':
            posts = chain(read_questions(), read_answers())
        elif sys.argv[1] == 'task1-topics':
            posts = read_topics()
        for post_id, post in posts:
            print(
                '"{}": {},'.format(
                    post_id,
                    json.dumps(post),
                ),
                file=f,
            )
        print('}', file=f)
