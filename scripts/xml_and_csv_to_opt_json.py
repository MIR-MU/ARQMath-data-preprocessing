# -*- coding:utf-8 -*-

import csv
import gzip
from itertools import chain
import json
from multiprocessing import Pool

from arqmathcode.post_reader_record import DataReaderRecord
from tqdm import tqdm

from .configuration import ARQMATH_COLLECTION_INPUT_DATA_DIRNAME, ARQMATH_COLLECTION_POSTS_OPT_FILENAME, POOL_NUM_WORKERS, POOL_CHUNKSIZE, ARQMATH_TRAIN_TSV_OPT_FILENAME, ARQMATH_TRAIN_TSV_OPT_NUM_FORMULAE, CSV_PARAMETERS
from .common import arqmath_post_read_html5_worker as read_html5_worker, Text, Math


def count_tsv():
    with open(ARQMATH_TRAIN_TSV_OPT_FILENAME, 'rt') as f:
        rows = csv.reader(f, **CSV_PARAMETERS)
        num_rows = sum(1 for _ in tqdm(rows, desc='Counting formulae')) - 1
    assert num_rows == ARQMATH_TRAIN_TSV_OPT_NUM_FORMULAE, '{} contains {} formulae instead of the expected {}'.format(
        ARQMATH_TRAIN_TSV_OPT_FILENAME,
        num_rows,
        ARQMATH_TRAIN_TSV_OPT_NUM_FORMULAE,
    )
    return num_rows


def read_tsv():
    with open(ARQMATH_TRAIN_TSV_OPT_FILENAME, 'rt') as f:
        rows = csv.reader(f, **CSV_PARAMETERS)
        next(rows)
        with Pool(POOL_NUM_WORKERS) as pool:
            for formula_id, math_tokens in pool.imap(read_tsv_worker, rows, POOL_CHUNKSIZE):
                yield (formula_id, math_tokens)


def read_tsv_worker(row):
    formula_id = int(row[0])
    math_tokens = list(map(Math, row[-1].split(' ')))
    return (formula_id, math_tokens)


MATH_FORMULAE = dict(tqdm(read_tsv(), total=count_tsv(), desc='Reading formulae'))
XML_READER = DataReaderRecord(ARQMATH_COLLECTION_INPUT_DATA_DIRNAME)


def read_posts(name, post_map):
    posts = (
        (post.post_id, post.body)
        for post
        in sorted(post_map.values(), key=lambda post: post.post_id)
    )
    converted_posts = tqdm(
        map(read_html5_worker, posts),
        total=len(post_map),
        desc='Converting {}'.format(name)
    )
    for post_id, input_document in converted_posts:
        output_document = []
        for input_token in input_document:
            output_tokens = []
            assert isinstance(input_token, (Text, tuple))
            if isinstance(input_token, Text):
                output_tokens = [str(input_token)]
            else:
                math_element_id, _ = input_token
                if math_element_id in MATH_FORMULAE:
                    output_tokens = list(map(str, MATH_FORMULAE[math_element_id]))
            output_document.extend(output_tokens)
        yield (post_id, output_document)


def read_questions():
    return read_posts('questions', XML_READER.post_parser.map_questions)


def read_answers():
    return read_posts('answers', XML_READER.post_parser.map_just_answers)


if __name__ == '__main__':
    with gzip.open(ARQMATH_COLLECTION_POSTS_OPT_FILENAME, 'wt') as f:
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
