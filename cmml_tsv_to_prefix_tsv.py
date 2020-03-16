#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from multiprocessing import Pool

from bs4 import BeautifulSoup
from tangentcft.TangentS.math_tan.math_extractor import MathExtractor
from tqdm import tqdm

from configuration import CSV_PARAMETERS, TSV_CMML_OUTPUT_NUM_ROWS, POOL_CHUNKSIZE, TSV_CMML_OUTPUT_FILENAME, TSV_PREFIX_FILENAME, TSV_PREFIX_FAILURES_FILENAME, POOL_NUM_WORKERS


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
        for cmml_row in cmml_rows:
            document = BeautifulSoup(cmml_row[-1], 'lxml')
            math_elements = document.find_all('math')
            if len(math_elements) >= 1:
                math_element = math_elements[0]
                math_element.semantics.unwrap()
                for share_element in math_element.find_all('share'):
                    share_element.decompose()
                math_tokens = str(math_element)
            else:
                math_tokens = ''
            yield cmml_row[:-1] + [math_tokens]


def write_tsv():
    cmml_rows = iter(tqdm(read_tsv(), total=count_tsv(), desc='Converting'))
    first_cmml_row = next(cmml_rows)
    with open(TSV_PREFIX_FILENAME, 'wt') as prefix_f:
        with open(TSV_PREFIX_FAILURES_FILENAME, 'wt') as prefix_failures_f:
            prefix_writer = csv.writer(prefix_f,  **CSV_PARAMETERS)
            prefix_writer.writerow(first_cmml_row)
            with Pool(POOL_NUM_WORKERS) as pool:
                num_successful, num_total = 0, 0
                for failure, prefix_row in pool.imap(write_tsv_worker, cmml_rows, POOL_CHUNKSIZE):
                    num_total += 1
                    if failure:
                        formula_number = prefix_row[0]
                        print('Processing formula #{} failed: {}'.format(formula_number, failure), file=prefix_failures_f)
                    else:
                        prefix_writer.writerow(prefix_row)
                        num_successful += 1
    print(
        'Successfully processed {} formulae out of {} ({:.2f}%)'.format(
            num_successful,
            num_total,
            100.0 * num_successful / num_total
        )
    )


def topological_sort(root):
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
    return visited_list


def write_tsv_worker(cmml_row):
    try:
        math_tree = MathExtractor.convert_to_semanticsymbol(cmml_row[-1])
        math_tokens = ' '.join(symbol.tag for symbol in topological_sort(math_tree))
        failure = None
    except Exception as e:
        math_tokens = ''
        failure = repr(e)
    return (failure, cmml_row[:-1] + [math_tokens])


if __name__ == '__main__':
    write_tsv()
