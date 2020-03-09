#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from io import TextIOWrapper
from multiprocessing import Pool
from zipfile import ZipFile

from bs4 import BeautifulSoup
from tangentcft.TangentS.math_tan.math_extractor import MathExtractor
from tqdm import tqdm

from configuration import CSV_PARAMETERS, TSV_PMML_NUM_ROWS, POOL_CHUNKSIZE, TSV_PMML_ZIP_FILENAME, TSV_PMML_FILENAME, TSV_SLT_FILENAME, TSV_SLT_FAILURES_FILENAME


def count_tsv():
    with ZipFile(TSV_PMML_ZIP_FILENAME, 'r') as zipfile:
        with zipfile.open(TSV_PMML_FILENAME, 'r') as f:
            rows = csv.reader(TextIOWrapper(f), **CSV_PARAMETERS)
            num_rows = sum(1 for _ in tqdm(rows, desc='Counting lines'))
    assert num_rows == TSV_PMML_NUM_ROWS, '{}/{} contains only {} formulae out of the expected {}'.format(
        TSV_PMML_ZIP_FILENAME,
        TSV_PMML_FILENAME,
        num_rows,
        TSV_PMML_NUM_ROWS,
    )
    return num_rows


def read_tsv():
    with ZipFile(TSV_PMML_ZIP_FILENAME, 'r') as zipfile:
        with zipfile.open(TSV_PMML_FILENAME, 'r') as f:
            pmml_rows = csv.reader(TextIOWrapper(f), **CSV_PARAMETERS)
            yield next(pmml_rows)
            for pmml_row in pmml_rows:
                document = BeautifulSoup(pmml_row[-1], 'lxml')
                math_elements = document.find_all('math')
                if len(math_elements) >= 1:
                    math_element = math_elements[0]
                    for share_element in math_element.find_all('share'):
                        share_element.decompose()
                    math_tokens = str(math_element)
                else:
                    math_tokens = ''
                yield pmml_row[:-1] + [math_tokens]


def write_tsv():
    pmml_rows = iter(tqdm(read_tsv(), total=count_tsv(), desc='Converting'))
    first_pmml_row = next(pmml_rows)
    with open(TSV_SLT_FILENAME, 'wt') as slt_f:
        with open(TSV_SLT_FAILURES_FILENAME, 'wt') as slt_failures_f:
            slt_writer = csv.writer(slt_f,  **CSV_PARAMETERS)
            slt_writer.writerow(first_pmml_row)
            with Pool(None) as pool:
                num_successful, num_total = 0, 0
                for failure, slt_row in pool.imap(write_tsv_worker, pmml_rows, POOL_CHUNKSIZE):
                    num_total += 1
                    if failure:
                        formula_number = slt_row[0]
                        print('Processing formula #{} failed: {}'.format(formula_number, failure), file=slt_failures_f)
                    else:
                        slt_writer.writerow(slt_row)
                        num_successful += 1
    print(
        'Successfully processed {} formulae out of {} ({:.2f}%)'.format(
            num_successful,
            num_total,
            100.0 * num_successful / num_total
        )
    )


def write_tsv_worker(pmml_row):
    try:
        math_tree = MathExtractor.convert_to_layoutsymbol(pmml_row[-1])
        math_tokens = '\t'.join((' '.join(edge) for edge in math_tree.get_pairs('', window=2, eob=True)))
        failure = None
    except Exception as e:
        math_tokens = ''
        failure = repr(e)
    return (failure, pmml_row[:-1] + [math_tokens])


if __name__ == '__main__':
    write_tsv()
