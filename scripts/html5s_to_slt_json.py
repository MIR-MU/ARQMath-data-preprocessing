#!/usr/bin/env python
# -*- coding:utf-8 -*-

import gzip
import json
from multiprocessing import Pool
import os.path
import sys
from zipfile import ZipFile

from lxml import etree
from tangentcft.TangentS.math_tan.math_extractor import MathExtractor
from tqdm import tqdm

from .common import ntcir_article_read_html5_worker as read_html5_worker, Text, Math, slt_tokenize as tokenize, unicode_to_tree, tree_to_unicode
from .configuration import POOL_NUM_WORKERS, POOL_CHUNKSIZE, ARXMLIV_NOPROBLEM_HTML5_ZIP_FILENAME, ARXMLIV_NOPROBLEM_JSON_SLT_FILENAME, ARXMLIV_NOPROBLEM_JSON_SLT_FAILURES_FILENAME, ARXMLIV_NOPROBLEM_HTML5_NUM_DOCUMENTS, ARXMLIV_WARNING1_HTML5_ZIP_FILENAME, ARXMLIV_WARNING1_JSON_SLT_FILENAME, ARXMLIV_WARNING1_JSON_SLT_FAILURES_FILENAME, ARXMLIV_WARNING1_HTML5_NUM_DOCUMENTS, ARXMLIV_WARNING2_HTML5_ZIP_FILENAME, ARXMLIV_WARNING2_JSON_SLT_FILENAME, ARXMLIV_WARNING2_JSON_SLT_FAILURES_FILENAME, ARXMLIV_WARNING2_HTML5_NUM_DOCUMENTS, XML_NAMESPACES


assert sys.argv[1] in ('no_problem', 'warning_1', 'warning_2')
if sys.argv[1] == 'no_problem':
    ARXMLIV_HTML5_ZIP_FILENAME = ARXMLIV_NOPROBLEM_HTML5_ZIP_FILENAME
    ARXMLIV_JSON_SLT_FILENAME = ARXMLIV_NOPROBLEM_JSON_SLT_FILENAME
    ARXMLIV_JSON_SLT_FAILURES_FILENAME = ARXMLIV_NOPROBLEM_JSON_SLT_FAILURES_FILENAME
    ARXMLIV_HTML5_NUM_DOCUMENTS = ARXMLIV_NOPROBLEM_HTML5_NUM_DOCUMENTS
elif sys.argv[1] == 'warning_1':
    ARXMLIV_HTML5_ZIP_FILENAME = ARXMLIV_WARNING_1_HTML5_ZIP_FILENAME
    ARXMLIV_JSON_SLT_FILENAME = ARXMLIV_WARNING_1_JSON_SLT_FILENAME
    ARXMLIV_JSON_SLT_FAILURES_FILENAME = ARXMLIV_WARNING_1_JSON_SLT_FAILURES_FILENAME
    ARXMLIV_HTML5_NUM_DOCUMENTS = ARXMLIV_WARNING_1_HTML5_NUM_DOCUMENTS
else:
    ARXMLIV_HTML5_ZIP_FILENAME = ARXMLIV_WARNING_2_HTML5_ZIP_FILENAME
    ARXMLIV_JSON_SLT_FILENAME = ARXMLIV_WARNING_2_JSON_SLT_FILENAME
    ARXMLIV_JSON_SLT_FAILURES_FILENAME = ARXMLIV_WARNING_2_JSON_SLT_FAILURES_FILENAME
    ARXMLIV_HTML5_NUM_DOCUMENTS = ARXMLIV_WARNING_2_HTML5_NUM_DOCUMENTS


def html5_filenames():
    with ZipFile(ARXMLIV_HTML5_ZIP_FILENAME, 'r') as zf:
        for filename in zf.namelist():
            if filename.endswith('.html'):
                yield (ARXMLIV_HTML5_ZIP_FILENAME, filename, False)


def count_html5s():
    num_documents = sum(1 for _ in tqdm(html5_filenames(), desc='Counting HTML5 documents'))
    assert num_documents == ARXMLIV_HTML5_NUM_DOCUMENTS, 'Archives contain {} documents instead of the expected {}'.format(
        num_documents,
        ARXMLIV_HTML5_NUM_DOCUMENTS,
    )
    return num_documents


def read_html5s():
    with Pool(POOL_NUM_WORKERS) as pool:
        for zip_filename, filename, document in pool.imap(read_html5_worker, html5_filenames(), POOL_CHUNKSIZE):
            yield (zip_filename, filename, document)


def write_json():
    documents = tqdm(read_html5s(), total=count_html5s(), desc='Converting')
    num_successful = 0
    num_total = 0
    with gzip.open(ARXMLIV_JSON_SLT_FILENAME, 'wt') as f, open(ARXMLIV_JSON_SLT_FAILURES_FILENAME, 'wt') as failures_f:
        print('{', file=f)
        with Pool(POOL_NUM_WORKERS) as pool:
            for partial_failure, zip_filename, filename, document in pool.imap(write_json_worker, documents, POOL_CHUNKSIZE):
                num_total += 1
                if partial_failure:
                    print(
                        'Processing HTML5 document {}/{} partially failed: \n{}'.format(
                            zip_filename,
                            filename,
                            partial_failure,
                        ),
                        file=failures_f
                    )
                else:
                    num_successful += 1
                for paragraph_number, paragraph in enumerate(document):
                    print(
                        '"{}_1_{}": {},'.format(
                            os.path.basename(filename)[:-5],
                            paragraph_number + 1,
                            json.dumps(paragraph),
                        ),
                        file=f,
                    )
        print('}', file=f)
    print(
        'Successfully processed {} HTML5 documents out of {} ({:.2f}%)'.format(
            num_successful,
            num_total,
            100.0 * num_successful / num_total
        )
    )


def write_json_worker(args):
    zip_filename, filename, input_paragraphs = args
    output_paragraphs = []
    partial_failure = []
    for input_paragraph_number, input_paragraph in enumerate(input_paragraphs):
        input_paragraph_number += 1
        output_paragraph = []
        input_math_token_number = 0
        for input_token in input_paragraph:
            assert isinstance(input_token, (Text, Math))
            if isinstance(input_token, Text):
                output_token = str(input_token)
                output_paragraph.append(output_token)
            else:
                input_math_token_number += 1
                try:
                    math_element = MathExtractor.isolate_pmml(input_token.math)
                    math_tree = unicode_to_tree(math_element)
                    etree.strip_elements(math_tree, '{{{}}}annotation'.format(XML_NAMESPACES['mathml']), with_tail=False)
                    math_element = tree_to_unicode(math_tree)
                    output_tokens = [
                        str(Math(token))
                        for token in tokenize(math_element)
                    ]
                    output_paragraph.extend(output_tokens)
                except Exception as e:
                    partial_failure.append(
                        '- Processing paragraph #{}, formula #{} failed: {}'.format(
                            input_paragraph_number,
                            input_math_token_number,
                            repr(e),
                        )
                    )
        output_paragraphs.append(output_paragraph)
    return ('\n'.join(partial_failure), zip_filename, filename, output_paragraphs)


if __name__ == '__main__':
    write_json()
