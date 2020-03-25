#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from multiprocessing import Pool

from bs4 import BeautifulSoup
from tangentcft.TangentS.math_tan.math_extractor import MathExtractor
from tqdm import tqdm

from .common import cmml_and_pmml_read_tsv_worker as read_tsv_worker, write_single_tsv as write_tsv
from .configuration import CSV_PARAMETERS, TSV_CMML_OUTPUT_NUM_ROWS, POOL_CHUNKSIZE, TSV_CMML_OUTPUT_FILENAME, TSV_PREFIX_FILENAME, TSV_PREFIX_FAILURES_FILENAME, POOL_NUM_WORKERS


def count_tsv():
    with open(TSV_CMML_OUTPUT_FILENAME, 'rt') as f:
        rows = csv.reader(f, **CSV_PARAMETERS)
        num_rows = sum(1 for _ in tqdm(rows, desc='Counting lines'))
    assert num_rows == TSV_CMML_OUTPUT_NUM_ROWS, '{} contains only {} formulae out of the expected {}'.format(
        TSV_CMML_OUTPUT_FILENAME,
        num_rows,
        TSV_CMML_OUTPUT_NUM_ROWS,
    )
    return num_rows


def read_tsv():
    with open(TSV_CMML_OUTPUT_FILENAME, 'rt') as f:
        cmml_rows = csv.reader(f, **CSV_PARAMETERS)
        yield next(cmml_rows)
        with Pool(POOL_NUM_WORKERS) as pool:
            for cmml_row in pool.imap(read_tsv_worker, cmml_rows, POOL_CHUNKSIZE):
                yield cmml_row


def prefix_tokenize_tree(root):
    visited_list = [root]
    visited_set = set(visited_list)
    stack = list(visited_list)
    while stack:
        node = stack[-1]
        if node not in visited_set:
            visited_list.append(node)
            visited_set.add(node)
        remove_from_stack = True
        for child in node.children or []:
            if child not in visited_set:
                stack.append(child)
                remove_from_stack = False
                break
        if remove_from_stack:
            stack.pop()
    return [node.tag for node in visited_list]


def write_tsv_worker(cmml_row):
    try:
        math_tree = MathExtractor.convert_to_semanticsymbol(cmml_row[-1])
        math_tokens = ' '.join(prefix_tokenize_tree(math_tree))
        failure = None
    except Exception as e:
        math_tokens = ''
        failure = repr(e)
    return (failure, cmml_row[:-1] + [math_tokens])


if __name__ == '__main__':
    write_tsv(count_tsv, read_tsv, write_tsv_worker, TSV_PREFIX_FILENAME, TSV_PREFIX_FAILURES_FILENAME)
