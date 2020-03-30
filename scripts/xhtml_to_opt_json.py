# -*- coding:utf-8 -*-

import json
from multiprocessing import Pool
import sys

from lxml import etree
from tangentcft.TangentS.math_tan.math_extractor import MathExtractor
from tqdm import tqdm

from .common import Math, Text, ntcir_topic_read_xhtml as read_xhtml, unicode_to_tree, opt_tokenize as tokenize
from .configuration import NTCIR11_MATH2_MAIN_TOPICS_XHTML_FILENAME, NTCIR11_MATH2_MAIN_TOPICS_JSON_OPT_FILENAME, NTCIR11_MATH2_MAIN_TOPICS_XHTML_NUM_TOPICS, NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_XHTML_FILENAME, NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_OPT_FILENAME, NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_XHTML_NUM_TOPICS, XML_NAMESPACES, NTCIR11_MATH2_MAIN_TOPICS_JSON_OPT_FAILURES_FILENAME, NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_OPT_FAILURES_FILENAME, POOL_NUM_WORKERS, POOL_CHUNKSIZE


assert sys.argv[1] in ('ntcir-11-math-2-main', 'ntcir-12-mathir-arxiv-main')
if sys.argv[1] == 'ntcir-11-math-2-main':
    TOPICS_XHTML_FILENAME = NTCIR11_MATH2_MAIN_TOPICS_XHTML_FILENAME
    TOPICS_XHTML_NUM_TOPICS = NTCIR11_MATH2_MAIN_TOPICS_XHTML_NUM_TOPICS
    TOPICS_JSON_OPT_FILENAME = NTCIR11_MATH2_MAIN_TOPICS_JSON_OPT_FILENAME
    TOPICS_JSON_OPT_FAILURES_FILENAME = NTCIR11_MATH2_MAIN_TOPICS_JSON_OPT_FAILURES_FILENAME
else:
    TOPICS_XHTML_FILENAME = NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_XHTML_FILENAME
    TOPICS_XHTML_NUM_TOPICS = NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_XHTML_NUM_TOPICS
    TOPICS_JSON_OPT_FILENAME = NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_OPT_FILENAME
    TOPICS_JSON_OPT_FAILURES_FILENAME = NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_OPT_FAILURES_FILENAME


def count_xhtml():
    xml_document = etree.parse(TOPICS_XHTML_FILENAME)
    num_topics = len(xml_document.xpath('//ntcir-math:topic', namespaces=XML_NAMESPACES))
    assert num_topics == TOPICS_XHTML_NUM_TOPICS, 'Document {} contains {} topics instead of the expected {}'.format(
        TOPICS_XHTML_FILENAME,
        num_topics,
        TOPICS_XHTML_NUM_TOPICS,
    )
    return num_topics


def write_json():
    topics = tqdm(read_xhtml(TOPICS_XHTML_FILENAME), total=count_xhtml(), desc='Converting')
    num_successful = 0
    num_total = 0
    with open(TOPICS_JSON_OPT_FILENAME, 'wt') as f, open(TOPICS_JSON_OPT_FAILURES_FILENAME, 'wt') as failures_f:
        print('{', file=f)
        with Pool(POOL_NUM_WORKERS) as pool:
            for partial_failure, topic_number, topic in pool.imap(write_json_worker, topics, POOL_CHUNKSIZE):
                num_total += 1
                if partial_failure:
                    print(
                        'Processing XHTML topic {} partially failed: \n{}'.format(
                            topic_number,
                            partial_failure,
                        ),
                        file=failures_f
                    )
                else:
                    num_successful += 1
                print(
                    '"{}": {},'.format(
                        topic_number,
                        json.dumps(topic),
                    ),
                    file=f,
                )
        print('}', file=f)
    print(
        'Successfully processed {} XHTML topics out of {} ({:.2f}%)'.format(
            num_successful,
            num_total,
            100.0 * num_successful / num_total
        )
    )


def write_json_worker(args):
    topic_number, input_tokens = args
    output_tokens = []
    partial_failure = []
    input_math_token_number = 0
    for input_token in input_tokens:
        assert isinstance(input_token, (Text, Math))
        if isinstance(input_token, Text):
            output_token = str(input_token)
            output_tokens.append(output_token)
        else:
            input_math_token_number += 1
            try:
                math_element = MathExtractor.isolate_cmml(input_token.math)
                output_math_tokens = [
                    str(Math(token))
                    for token in tokenize(math_element)
                ]
                output_tokens.extend(output_math_tokens)
            except Exception as e:
                partial_failure.append(
                    '- Processing formula #{} failed: {}'.format(
                        input_math_token_number,
                        repr(e),
                    )
                )
    return ('\n'.join(partial_failure), topic_number, output_tokens)


if __name__ == '__main__':
    write_json()
