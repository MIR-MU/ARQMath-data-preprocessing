# -*- coding:utf-8 -*-

import csv
from copy import copy

from bs4 import BeautifulSoup
from multiprocessing import Pool
from tqdm import tqdm

from .configuration import POOL_NUM_WORKERS, POOL_CHUNKSIZE, CSV_PARAMETERS


def cmml_read_tsv_worker(cmml_row):
    document = BeautifulSoup(cmml_row[-1], 'lxml')
    math_elements = document.find_all('math')
    if len(math_elements) >= 1:
        math_element = math_elements[0]
        math_element.semantics.unwrap()  # remove <semantics> element
        for share_element in math_element.find_all('share'):  # resolve <share> elements
            assert share_element['href'].startswith('#')
            shared_element = math_element.find(id=share_element['href'][1:])
            if shared_element:
                share_element.replace_with(copy(shared_element))
            else:
                share_element.decompose()
        math_tokens = str(math_element)
    else:
        math_tokens = ''
    return cmml_row[:-1] + [math_tokens]


def pmml_read_tsv_worker(pmml_row):
    document = BeautifulSoup(pmml_row[-1], 'lxml')
    math_elements = document.find_all('math')
    if len(math_elements) >= 1:
        math_element = math_elements[0]
        for share_element in math_element.find_all('share'):  # resolve <share> elements
            assert share_element['href'].startswith('#')
            shared_element = math_element.find(id=share_element['href'][1:])
            if shared_element:
                share_element.replace_with(copy(shared_element))
            else:
                share_element.decompose()
        math_tokens = str(math_element)
    else:
        math_tokens = ''
    return pmml_row[:-1] + [math_tokens]


def write_single_tsv(count_tsv, read_tsv, write_tsv_worker, output_tsv_filename, output_failures_filename):
    rows = iter(tqdm(read_tsv(), total=count_tsv(), desc='Converting'))
    first_row = next(rows)
    with open(output_tsv_filename, 'wt') as tsv_f:
        with open(output_failures_filename, 'wt') as failures_f:
            prefix_writer = csv.writer(tsv_f,  **CSV_PARAMETERS)
            prefix_writer.writerow(first_row)
            with Pool(POOL_NUM_WORKERS) as pool:
                num_successful, num_total = 0, 0
                for failure, prefix_row in pool.imap(write_tsv_worker, rows, POOL_CHUNKSIZE):
                    num_total += 1
                    if failure:
                        formula_number = prefix_row[0]
                        print('Processing formula #{} failed: {}'.format(formula_number, failure), file=failures_f)
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
