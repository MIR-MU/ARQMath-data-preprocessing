#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from multiprocessing import Pool
import sys

from bs4 import BeautifulSoup
from tqdm import tqdm

from .common import cmml_and_pmml_read_tsv_worker as read_tsv_worker, write_single_tsv as write_tsv, infix_tokenize as tokenize
from .configuration import CSV_PARAMETERS, ARQMATH_TRAIN_TSV_CMML_OUTPUT_NUM_ROWS, POOL_CHUNKSIZE, ARQMATH_TRAIN_TSV_CMML_OUTPUT_FILENAME, ARQMATH_TRAIN_TSV_INFIX_FILENAME, ARQMATH_TRAIN_TSV_INFIX_FAILURES_FILENAME, POOL_NUM_WORKERS, TSV_OPT_INFIX_OPERATORS, ARQMATH_TEST_TSV_CMML_OUTPUT_FILENAME, ARQMATH_TEST_TSV_INFIX_FILENAME, ARQMATH_TEST_TSV_INFIX_FAILURES_FILENAME, ARQMATH_TEST_TSV_CMML_OUTPUT_NUM_ROWS


if sys.argv[1] == 'train':
    ARQMATH_TSV_CMML_OUTPUT_FILENAME = ARQMATH_TRAIN_TSV_CMML_OUTPUT_FILENAME
    ARQMATH_TSV_CMML_OUTPUT_NUM_ROWS = ARQMATH_TRAIN_TSV_CMML_OUTPUT_NUM_ROWS
    ARQMATH_TSV_INFIX_FILENAME = ARQMATH_TRAIN_TSV_INFIX_FILENAME
    ARQMATH_TSV_INFIX_FAILURES_FILENAME = ARQMATH_TRAIN_TSV_INFIX_FAILURES_FILENAME
else:
    ARQMATH_TSV_CMML_OUTPUT_FILENAME = ARQMATH_TEST_TSV_CMML_OUTPUT_FILENAME
    ARQMATH_TSV_CMML_OUTPUT_NUM_ROWS = ARQMATH_TEST_TSV_CMML_OUTPUT_NUM_ROWS
    ARQMATH_TSV_INFIX_FILENAME = ARQMATH_TEST_TSV_INFIX_FILENAME
    ARQMATH_TSV_INFIX_FAILURES_FILENAME = ARQMATH_TEST_TSV_INFIX_FAILURES_FILENAME


def count_tsv():
    with open(ARQMATH_TSV_CMML_OUTPUT_FILENAME, 'rt') as f:
        rows = csv.reader(f, **CSV_PARAMETERS)
        num_rows = sum(1 for _ in tqdm(rows, desc='Counting lines'))
    assert num_rows == ARQMATH_TSV_CMML_OUTPUT_NUM_ROWS, '{} contains {} formulae instead of the expected {}'.format(
        ARQMATH_TSV_CMML_OUTPUT_FILENAME,
        num_rows,
        ARQMATH_TSV_CMML_OUTPUT_NUM_ROWS,
    )
    return num_rows


def read_tsv():
    with open(ARQMATH_TSV_CMML_OUTPUT_FILENAME, 'rt') as f:
        cmml_rows = csv.reader(f, **CSV_PARAMETERS)
        yield next(cmml_rows)
        with Pool(POOL_NUM_WORKERS) as pool:
            for cmml_row in pool.imap(read_tsv_worker, cmml_rows, POOL_CHUNKSIZE):
                yield cmml_row


def write_tsv_worker(cmml_row):
    try:
        math_tokens = ' '.join(tokenize(cmml_row[-1]))
        failure = None
    except Exception as e:
        math_tokens = ''
        failure = repr(e)
    return (failure, cmml_row[:-1] + [math_tokens])


if __name__ == '__main__':
    write_tsv(count_tsv, read_tsv, write_tsv_worker, ARQMATH_TSV_INFIX_FILENAME, ARQMATH_TSV_INFIX_FAILURES_FILENAME)
