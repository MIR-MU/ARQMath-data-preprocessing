# -*- coding:utf-8 -*-

import csv
from copy import copy
import subprocess

from bs4 import BeautifulSoup
from lxml import etree
from multiprocessing import Pool
from tqdm import tqdm

from .configuration import POOL_NUM_WORKERS, POOL_CHUNKSIZE, CSV_PARAMETERS, ETREE_TOSTRING_PARAMETERS, LATEXMLC, MATHMLCAN


def unicode_to_tree(text):
    return etree.XML(text.encode(ETREE_TOSTRING_PARAMETERS['encoding']))


def tree_to_unicode(tree):
    return etree.tostring(tree, **ETREE_TOSTRING_PARAMETERS).decode(ETREE_TOSTRING_PARAMETERS['encoding'])


def latexml(latex_input):
    latex_input = latex_input.encode('utf-8')
    xml_output = subprocess.Popen(
        LATEXMLC,
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ).communicate(latex_input)[0]
    xml_output = xml_output.decode('utf-8')
    return xml_output


def mathmlcan(xml_input):
    xml_input = resolve_share_elements(xml_input)
    xml_input = xml_input.encode('utf-8')
    xml_output = subprocess.Popen(
        MATHMLCAN,
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ).communicate(xml_input)[0]
    xml_output = xml_output.decode('utf-8')
    return xml_output


def resolve_share_elements(math_tokens):
    math_element = BeautifulSoup(math_tokens, 'lxml')
    for share_element in math_element.find_all('share'):
        assert share_element['href'].startswith('#')
        shared_element = math_element.find(id=share_element['href'][1:])
        if shared_element:
            share_element.replace_with(copy(shared_element))
        else:
            share_element.decompose()
    return str(math_element)


def cmml_and_pmml_read_tsv_worker(row):
    document = BeautifulSoup(row[-1], 'lxml')
    math_elements = document.find_all('math')
    if len(math_elements) >= 1:
        math_element = math_elements[0]
        math_tokens = str(math_element)
    else:
        math_tokens = ''
    return row[:-1] + [math_tokens]


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
