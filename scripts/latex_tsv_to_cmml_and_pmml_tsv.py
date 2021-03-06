#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from itertools import islice
from io import TextIOWrapper
from os.path import join
from multiprocessing import Pool
import re
import subprocess
import sys
from zipfile import ZipFile

from bs4 import BeautifulSoup
from lxml import etree
from tqdm import tqdm
from tangentcft.TangentS.math_tan.math_extractor import MathExtractor

from .configuration import CSV_PARAMETERS, LATEXMLC_BATCH_SIZE, LATEXMLC, ARQMATH_TRAIN_TSV_LATEX_ZIP_FILENAME, POOL_CHUNKSIZE, ARQMATH_TRAIN_TSV_CMML_OUTPUT_FILENAME, ARQMATH_TRAIN_TSV_PMML_OUTPUT_FILENAME, ARQMATH_TRAIN_TSV_LATEX_NUM_FORMULAE, ARQMATH_TRAIN_TSV_CMML_OUTPUT_FAILURES_FILENAME, ARQMATH_TRAIN_TSV_PMML_OUTPUT_FAILURES_FILENAME, XML_NAMESPACES, POOL_NUM_WORKERS, ARQMATH_TASK1_TEST_TSV_LATEX_FILENAME, ARQMATH_TASK1_TEST_TSV_CMML_OUTPUT_FILENAME, ARQMATH_TASK1_TEST_TSV_CMML_OUTPUT_FAILURES_FILENAME, ARQMATH_TASK1_TEST_TSV_PMML_OUTPUT_FILENAME, ARQMATH_TASK1_TEST_TSV_PMML_OUTPUT_FAILURES_FILENAME, ARQMATH_TASK1_TEST_TSV_LATEX_NUM_FORMULAE, ARQMATH_TASK1_VALIDATION_TSV_LATEX_FILENAME, ARQMATH_TASK1_VALIDATION_TSV_LATEX_NUM_FORMULAE, ARQMATH_TASK1_VALIDATION_TSV_CMML_OUTPUT_FILENAME, ARQMATH_TASK1_VALIDATION_TSV_CMML_OUTPUT_FAILURES_FILENAME, ARQMATH_TASK1_VALIDATION_TSV_PMML_OUTPUT_FILENAME, ARQMATH_TASK1_VALIDATION_TSV_PMML_OUTPUT_FAILURES_FILENAME, ARQMATH_TASK2_TEST_TSV_LATEX_FILENAME, ARQMATH_TASK2_TEST_TSV_CMML_OUTPUT_FILENAME, ARQMATH_TASK2_TEST_TSV_CMML_OUTPUT_FAILURES_FILENAME, ARQMATH_TASK2_TEST_TSV_PMML_OUTPUT_FILENAME, ARQMATH_TASK2_TEST_TSV_PMML_OUTPUT_FAILURES_FILENAME, ARQMATH_TASK2_TEST_TSV_LATEX_NUM_FORMULAE
from .common import tree_to_unicode, unicode_to_tree, latexml, mathmlcan


assert sys.argv[1] in ('train', 'task1-validation', 'task1-test', 'task2-test')
if sys.argv[1] == 'train':
    ARQMATH_TSV_LATEX_FILENAME = ARQMATH_TRAIN_TSV_LATEX_ZIP_FILENAME
    ARQMATH_TSV_LATEX_NUM_FORMULAE = ARQMATH_TRAIN_TSV_LATEX_NUM_FORMULAE
    ARQMATH_TSV_CMML_OUTPUT_FILENAME = ARQMATH_TRAIN_TSV_CMML_OUTPUT_FILENAME
    ARQMATH_TSV_CMML_OUTPUT_FAILURES_FILENAME = ARQMATH_TRAIN_TSV_CMML_OUTPUT_FAILURES_FILENAME
    ARQMATH_TSV_PMML_OUTPUT_FILENAME = ARQMATH_TRAIN_TSV_PMML_OUTPUT_FILENAME
    ARQMATH_TSV_PMML_OUTPUT_FAILURES_FILENAME = ARQMATH_TRAIN_TSV_PMML_OUTPUT_FAILURES_FILENAME
elif sys.argv[1] == 'task1-validation':
    ARQMATH_TSV_LATEX_FILENAME = ARQMATH_TASK1_VALIDATION_TSV_LATEX_FILENAME
    ARQMATH_TSV_LATEX_NUM_FORMULAE = ARQMATH_TASK1_VALIDATION_TSV_LATEX_NUM_FORMULAE
    ARQMATH_TSV_CMML_OUTPUT_FILENAME = ARQMATH_TASK1_VALIDATION_TSV_CMML_OUTPUT_FILENAME
    ARQMATH_TSV_CMML_OUTPUT_FAILURES_FILENAME = ARQMATH_TASK1_VALIDATION_TSV_CMML_OUTPUT_FAILURES_FILENAME
    ARQMATH_TSV_PMML_OUTPUT_FILENAME = ARQMATH_TASK1_VALIDATION_TSV_PMML_OUTPUT_FILENAME
    ARQMATH_TSV_PMML_OUTPUT_FAILURES_FILENAME = ARQMATH_TASK1_VALIDATION_TSV_PMML_OUTPUT_FAILURES_FILENAME
elif sys.argv[1] == 'task1-test':
    ARQMATH_TSV_LATEX_FILENAME = ARQMATH_TASK1_TEST_TSV_LATEX_FILENAME
    ARQMATH_TSV_LATEX_NUM_FORMULAE = ARQMATH_TASK1_TEST_TSV_LATEX_NUM_FORMULAE
    ARQMATH_TSV_CMML_OUTPUT_FILENAME = ARQMATH_TASK1_TEST_TSV_CMML_OUTPUT_FILENAME
    ARQMATH_TSV_CMML_OUTPUT_FAILURES_FILENAME = ARQMATH_TASK1_TEST_TSV_CMML_OUTPUT_FAILURES_FILENAME
    ARQMATH_TSV_PMML_OUTPUT_FILENAME = ARQMATH_TASK1_TEST_TSV_PMML_OUTPUT_FILENAME
    ARQMATH_TSV_PMML_OUTPUT_FAILURES_FILENAME = ARQMATH_TASK1_TEST_TSV_PMML_OUTPUT_FAILURES_FILENAME
else:
    ARQMATH_TSV_LATEX_FILENAME = ARQMATH_TASK2_TEST_TSV_LATEX_FILENAME
    ARQMATH_TSV_LATEX_NUM_FORMULAE = ARQMATH_TASK2_TEST_TSV_LATEX_NUM_FORMULAE
    ARQMATH_TSV_CMML_OUTPUT_FILENAME = ARQMATH_TASK2_TEST_TSV_CMML_OUTPUT_FILENAME
    ARQMATH_TSV_CMML_OUTPUT_FAILURES_FILENAME = ARQMATH_TASK2_TEST_TSV_CMML_OUTPUT_FAILURES_FILENAME
    ARQMATH_TSV_PMML_OUTPUT_FILENAME = ARQMATH_TASK2_TEST_TSV_PMML_OUTPUT_FILENAME
    ARQMATH_TSV_PMML_OUTPUT_FAILURES_FILENAME = ARQMATH_TASK2_TEST_TSV_PMML_OUTPUT_FAILURES_FILENAME


def get_batches(iterable, batch_size=LATEXMLC_BATCH_SIZE):
    iterator = iter(iterable)
    return iter(lambda: tuple(islice(iterator, batch_size)), ())


def count_tsv():
    if ARQMATH_TSV_LATEX_FILENAME.endswith('.zip'):
        with ZipFile(ARQMATH_TSV_LATEX_FILENAME, 'r') as zf:
            num_rows = 0
            for filename in tqdm(zf.namelist(), desc='Counting formulae'):
                if filename.endswith('.tsv'):
                    with zf.open(filename, 'r') as f:
                        rows = csv.reader(TextIOWrapper(f), **CSV_PARAMETERS)
                        num_rows += sum(1 for _ in rows) - 1
    else:
        with open(ARQMATH_TSV_LATEX_FILENAME, 'rt') as f:
            rows = csv.reader(f, **CSV_PARAMETERS)
            num_rows = sum(1 for _ in tqdm(rows, desc='Counting formulae')) - 1
    assert num_rows == ARQMATH_TSV_LATEX_NUM_FORMULAE, '{} contains {} formulae instead of the expected {}'.format(
        ARQMATH_TSV_LATEX_FILENAME,
        num_rows,
        ARQMATH_TSV_LATEX_NUM_FORMULAE,
    )
    return num_rows


def read_tsv():
    if ARQMATH_TSV_LATEX_FILENAME.endswith('.zip'):
        with ZipFile(ARQMATH_TSV_LATEX_FILENAME, 'r') as zf:
            first_file = True
            for filename in zf.namelist():
                if filename.endswith('.tsv'):
                    with zf.open(filename, 'r') as f:
                        latex_rows = csv.reader(TextIOWrapper(f), **CSV_PARAMETERS)
                        if first_file:
                            yield next(latex_rows)
                            first_file = False
                        else:
                            next(latex_rows)
                        for latex_row in latex_rows:
                            math_tokens = re.sub(r'([^\\])%', r'\1', latex_row[-1])
                            yield latex_row[:-1] + [math_tokens]
    else:
        with open(ARQMATH_TSV_LATEX_FILENAME, 'rt') as f:
            latex_rows = csv.reader(f, **CSV_PARAMETERS)
            yield next(latex_rows)
            for latex_row in latex_rows:
                math_tokens = re.sub(r'([^\\])%', r'\1', latex_row[-1])
                yield latex_row[:-1] + [math_tokens]


def write_tsv():
    latex_rows = iter(tqdm(read_tsv(), total=count_tsv(), desc='Converting'))
    first_latex_row = next(latex_rows)
    with open(ARQMATH_TSV_CMML_OUTPUT_FILENAME, 'wt') as cmml_f, open(ARQMATH_TSV_CMML_OUTPUT_FAILURES_FILENAME, 'wt') as cmml_failures_f:
        cmml_num_successful = 0
        cmml_writer = csv.writer(cmml_f,  **CSV_PARAMETERS)
        cmml_writer.writerow(first_latex_row)
        with open(ARQMATH_TSV_PMML_OUTPUT_FILENAME, 'wt') as pmml_f, open(ARQMATH_TSV_PMML_OUTPUT_FAILURES_FILENAME, 'wt') as pmml_failures_f:
            pmml_num_successful = 0
            pmml_writer = csv.writer(pmml_f,  **CSV_PARAMETERS)
            pmml_writer.writerow(first_latex_row)
            with Pool(POOL_NUM_WORKERS * 2) as pool:
                num_total = 0
                for cmml_rows, pmml_rows in pool.imap(write_tsv_worker, get_batches(latex_rows), POOL_CHUNKSIZE):
                    assert len(cmml_rows) == len(pmml_rows)
                    num_total += len(cmml_rows)
                    for cmml_failure, cmml_row in cmml_rows:
                        if cmml_failure:
                            print('Processing CMML formula #{} failed: {}'.format(cmml_row[0], cmml_failure), file=cmml_failures_f)
                        else:
                            cmml_writer.writerow(cmml_row)
                            cmml_num_successful += 1
                    for pmml_failure, pmml_row in pmml_rows:
                        if pmml_failure:
                            print('Processing PMML formula #{} failed: {}'.format(pmml_row[0], pmml_failure), file=pmml_failures_f)
                        else:
                            pmml_writer.writerow(pmml_row)
                            pmml_num_successful += 1
    print(
        'Successfully processed {} CMML formulae out of {} ({:.2f}%)'.format(
            cmml_num_successful,
            num_total,
            100.0 * cmml_num_successful / num_total
        )
    )
    print(
        'Successfully processed {} PMML formulae out of {} ({:.2f}%)'.format(
            pmml_num_successful,
            num_total,
            100.0 * pmml_num_successful / num_total
        )
    )


def write_tsv_worker(latex_rows):
    latex_input = '\n\n'.join(
        'Formula #{}:\n\[{}\]'.format(latex_row[0], latex_row[-1])
        for latex_row in latex_rows
    )
    cmml_rows = []
    pmml_rows = []
    try:
        xml_output = mathmlcan(latexml(latex_input))
        try:
            xml_document = unicode_to_tree(xml_output)
            for latex_row in latex_rows:
                math_elements = xml_document.xpath(
                    '//xhtml:div[@class = "ltx_para" and xhtml:p[@class = "ltx_p" and normalize-space(text()) = "Formula #{}:"]]//mathml:math'.format(latex_row[0]),
                    namespaces=XML_NAMESPACES
                )
                if len(math_elements) >= 1:
                    math_element = math_elements[0]
                    math_tokens = tree_to_unicode(math_element)
                    try:
                        cmml_math_element = unicode_to_tree(MathExtractor.isolate_cmml(math_tokens))
                        pmml_math_element = unicode_to_tree(MathExtractor.isolate_pmml(math_tokens))
                        if cmml_math_element.xpath('//mathml:cerror', namespaces=XML_NAMESPACES):
                            cmml_math_tokens = ''
                            cmml_failure = ValueError('LaTeXML output contains <cerror> elements')
                        else:
                            etree.strip_tags(cmml_math_element, '{{{}}}semantics'.format(XML_NAMESPACES['mathml']))
                            cmml_math_tokens = tree_to_unicode(cmml_math_element)
                            cmml_failure = None
                        if pmml_math_element.xpath('//mathml:cerror', namespaces=XML_NAMESPACES):
                            pmml_math_tokens = ''
                            pmml_failure = ValueError('LaTeXML output contains <cerror> elements')
                        else:
                            pmml_math_tokens = tree_to_unicode(pmml_math_element)
                            pmml_failure = None
                    except Exception as e:
                        cmml_math_tokens = ''
                        pmml_math_tokens = ''
                        cmml_failure = e
                        pmml_failure = e
                else:
                    cmml_math_tokens = ''
                    pmml_math_tokens = ''
                    cmml_failure = ValueError('Formula not found in LaTeXML output')
                    pmml_failure = ValueError('Formula not found in LaTeXML output')
                cmml_row = latex_row[:-1] + [cmml_math_tokens]
                pmml_row = latex_row[:-1] + [pmml_math_tokens]
                cmml_rows.append((cmml_failure, cmml_row))
                pmml_rows.append((pmml_failure, pmml_row))
        except etree.Error as e:  # LaTeXML conversion failed, try halving latex_rows
            assert len(latex_rows) > 0
            if len(latex_rows) > 1:
#               starting_formula_number = latex_rows[0][0]
#               ending_formula_number = latex_rows[len(latex_rows) // 2 - 1][0]
#               print('Splitting formulae from {} to {}'.format(starting_formula_number, ending_formula_number))
                latex_rows_head = latex_rows[:len(latex_rows) // 2]
                latex_rows_tail = latex_rows[len(latex_rows) // 2:]
                cmml_rows_head, pmml_rows_head = write_tsv_worker(latex_rows_head)
                cmml_rows_tail, pmml_rows_tail = write_tsv_worker(latex_rows_tail)
                cmml_rows.extend(cmml_rows_head + cmml_rows_tail)
                pmml_rows.extend(pmml_rows_head + pmml_rows_tail)
            else:
                latex_row = latex_rows[0]
                cmml_math_tokens = ''
                pmml_math_tokens = ''
                cmml_row = latex_row[:-1] + [cmml_math_tokens]
                pmml_row = latex_row[:-1] + [pmml_math_tokens]
                cmml_failure = ValueError(e.msg)
                pmml_failure = ValueError(e.msg)
                cmml_rows.append((cmml_failure, cmml_row))
                pmml_rows.append((pmml_failure, pmml_row))
    except subprocess.SubprocessError as e:
        cmml_math_tokens = ''
        pmml_math_tokens = ''
        cmml_failure = e
        pmml_failure = e
        for latex_row in latex_rows:
            cmml_row = latex_row[:-1] + [cmml_math_tokens]
            pmml_row = latex_row[:-1] + [pmml_math_tokens]
            cmml_rows.append((cmml_failure, cmml_row))
            pmml_rows.append((pmml_failure, pmml_row))
    return (cmml_rows, pmml_rows)


if __name__ == '__main__':
    write_tsv()
