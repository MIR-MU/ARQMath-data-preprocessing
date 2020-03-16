#!/usr/bin/env python
# -*- coding:utf-8 -*-

from copy import copy
import csv
from multiprocessing import Pool

from bs4 import BeautifulSoup
from tangentcft.TangentS.math_tan.math_extractor import MathExtractor
from tqdm import tqdm

from .common import cmml_read_tsv_worker as read_tsv_worker, write_single_tsv as write_tsv
from .configuration import CSV_PARAMETERS, TSV_CMML_OUTPUT_NUM_ROWS, POOL_CHUNKSIZE, TSV_CMML_OUTPUT_FILENAME, TSV_INFIX_FILENAME, TSV_INFIX_FAILURES_FILENAME, POOL_NUM_WORKERS, TSV_OPT_INFIX_OPERATORS


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


def infix_tokenize_tree(root):
    result = []
    stack = [[root, 0]]
    while stack:
        node, child_index = stack.pop()
        num_children = len(node.children or [])
        node_visited = child_index > 0
        node_completed = child_index == num_children
        if not node_visited:
            if node.tag not in TSV_OPT_INFIX_OPERATORS or num_children < 2:
                result.append(node.tag)
            if num_children > 0:
                result.append('(')
        else:
            if not node_completed:
                if node.tag not in TSV_OPT_INFIX_OPERATORS:
                    result.append(',')
                else:
                    result.append(node.tag)
            else:
                result.append(')')
        if not node_completed:
            child_node = node.children[child_index]
            stack.append((node, child_index + 1))
            stack.append((child_node, 0))
    return result


def write_tsv_worker(cmml_row):
    try:
        math_tree = MathExtractor.convert_to_semanticsymbol(cmml_row[-1])
        math_tokens = ' '.join(infix_tokenize_tree(math_tree))
        failure = None
    except Exception as e:
        math_tokens = ''
        failure = repr(e)
    return (failure, cmml_row[:-1] + [math_tokens])


if __name__ == '__main__':
    write_tsv(count_tsv, read_tsv, write_tsv_worker, TSV_INFIX_FILENAME, TSV_INFIX_FAILURES_FILENAME)
