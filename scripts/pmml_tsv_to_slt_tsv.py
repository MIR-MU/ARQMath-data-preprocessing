#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from multiprocessing import Pool

from bs4 import BeautifulSoup
from tqdm import tqdm

from .common import pmml_read_tsv_worker as read_tsv_worker, write_single_tsv as write_tsv, slt_tokenize as tokenize
from .configuration import CSV_PARAMETERS, ARQMATH_TRAIN_TSV_PMML_OUTPUT_NUM_ROWS, POOL_CHUNKSIZE, ARQMATH_TRAIN_TSV_PMML_OUTPUT_FILENAME, ARQMATH_TRAIN_TSV_SLT_FILENAME, ARQMATH_TRAIN_TSV_SLT_FAILURES_FILENAME, POOL_NUM_WORKERS


def count_tsv():
    with open(ARQMATH_TRAIN_TSV_PMML_OUTPUT_FILENAME, 'rt') as f:
        rows = csv.reader(f, **CSV_PARAMETERS)
        num_rows = sum(1 for _ in tqdm(rows, desc='Counting lines'))
    assert num_rows == ARQMATH_TRAIN_TSV_PMML_OUTPUT_NUM_ROWS, '{} contains {} formulae instead of the expected {}'.format(
        ARQMATH_TRAIN_TSV_PMML_OUTPUT_FILENAME,
        num_rows,
        ARQMATH_TRAIN_TSV_PMML_OUTPUT_NUM_ROWS,
    )
    return num_rows


def read_tsv():
    with open(ARQMATH_TRAIN_TSV_PMML_OUTPUT_FILENAME, 'rt') as f:
        pmml_rows = csv.reader(f, **CSV_PARAMETERS)
        yield next(pmml_rows)
        with Pool(POOL_NUM_WORKERS) as pool:
            for pmml_row in pool.imap(read_tsv_worker, pmml_rows, POOL_CHUNKSIZE):
                yield pmml_row


def write_tsv_worker(pmml_row):
    try:
        math_tokens = ' '.join(tokenize(pmml_row[-1]))
        failure = None
    except Exception as e:
        math_tokens = ''
        failure = repr(e)
    return (failure, pmml_row[:-1] + [math_tokens])


if __name__ == '__main__':
    write_tsv(count_tsv, read_tsv, write_tsv_worker, ARQMATH_TRAIN_TSV_SLT_FILENAME, ARQMATH_TRAIN_TSV_SLT_FAILURES_FILENAME)
