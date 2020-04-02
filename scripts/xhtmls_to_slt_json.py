#!/usr/bin/env python
# -*- coding:utf-8 -*-

from glob import glob
import gzip
import json
from multiprocessing import Pool

from tangentcft.TangentS.math_tan.math_extractor import MathExtractor
from tqdm import tqdm
import sys

from .common import ntcir_article_read_xhtml_worker as read_xhtml_worker, Math, slt_tokenize as tokenize
from .configuration import POOL_NUM_WORKERS, POOL_CHUNKSIZE, NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_XHTML_GLOB, NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_SLT_FILENAME, NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_SLT_FAILURES_FILENAME, NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_XHTML_NUM_DOCUMENTS, XML_NAMESPACES


def xhtml_filenames():
    for filename in glob(NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_XHTML_GLOB):
        yield filename


def count_xhtmls():
    num_documents = sum(1 for _ in tqdm(xhtml_filenames(), desc='Counting XHTML documents'))
    assert num_documents == NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_XHTML_NUM_DOCUMENTS, 'Archives contain {} documents instead of the expected {}'.format(
        num_documents,
        ARXMLIV_HTML5_NUM_DOCUMENTS,
    )
    return num_documents


def read_xhtmls():
    with Pool(POOL_NUM_WORKERS) as pool:
        for filename, formulae in pool.imap(read_xhtml_worker, xhtml_filenames(), POOL_CHUNKSIZE):
            yield (filename, formulae)


def write_json():
    documents = tqdm(read_xhtmls(), total=count_xhtmls(), desc='Converting')
    num_successful = 0
    num_total = 0
    with gzip.open(NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_SLT_FILENAME, 'wt') as f, open(NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_SLT_FAILURES_FILENAME, 'wt') as failures_f:
        print('{', file=f)
        with Pool(POOL_NUM_WORKERS) as pool:
            for partial_failure, filename, formulae in pool.imap(write_json_worker, documents, POOL_CHUNKSIZE):
                num_total += 1
                if partial_failure:
                    print(
                        'Processing XHTML document {} partially failed: \n{}'.format(
                            filename,
                            partial_failure,
                        ),
                        file=failures_f
                    )
                else:
                    num_successful += 1
                for formula_id, formula in formulae:
                    print(
                        '"{}": {},'.format(
                            formula_id,
                            json.dumps(formula),
                        ),
                        file=f,
                    )
        print('}', file=f)
    print(
        'Successfully processed {} XHTML documents out of {} ({:.2f}%)'.format(
            num_successful,
            num_total,
            100.0 * num_successful / num_total
        )
    )


def write_json_worker(args):
    filename, input_formulae = args
    output_formulae = []
    partial_failure = []
    for input_formula_id, input_formula in input_formulae:
        output_formula_id = input_formula_id
        try:
            math_element = MathExtractor.isolate_pmml(input_formula.math)
            output_formula = [
                str(Math(token))
                for token in tokenize(math_element)
            ]
            output_formulae.append((output_formula_id, output_formula))
        except Exception as e:
            partial_failure.append(
                '- Processing formula {} failed: {}'.format(
                    input_formula_id,
                    repr(e),
                )
            )
    return ('\n'.join(partial_failure), filename, output_formulae)


if __name__ == '__main__':
    write_json()
