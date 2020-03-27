# -*- coding:utf-8 -*-

import csv
from copy import copy
from multiprocessing import Pool
import re
import subprocess
from zipfile import ZipFile

from bs4 import BeautifulSoup
from gensim.utils import simple_preprocess
from lxml import etree
import n2w
from tangentcft.TangentS.math_tan.math_extractor import MathExtractor
from tqdm import tqdm

from .configuration import POOL_NUM_WORKERS, POOL_CHUNKSIZE, CSV_PARAMETERS, XML_NAMESPACES, ETREE_TOSTRING_PARAMETERS, LATEXMLC, MATHMLCAN, TSV_OPT_INFIX_OPERATORS


class Text(object):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return 'text:{}'.format(self.text)

    def __repr__(self):
        return '{}'.format(self.text)


class Math(object):
    def __init__(self, math):
        self.math = math

    def __str__(self):
        return 'math:{}'.format(self.math)

    def __repr__(self):
        return '{{Math: {} ...}}'.format(self.math[:10])


def read_xhtml_worker(args):
    zip_filename, filename = args
    with ZipFile(zip_filename, 'r') as zf:
        with zf.open(filename, 'r') as f:
            html5_parser = etree.HTMLParser()
            xml_document = etree.parse(f, html5_parser)
            math_tokens = {}
            for math_element_number, math_element in enumerate(xml_document.xpath('//p/math')):
                math_element_token = 'math_element_{}___'.format(
                    re.sub(r'\s+', '_', n2w.convert(math_element_number))
                )
                replacement = etree.Element("span")
                replacement.text = math_element_token
                math_element.getparent().replace(math_element, replacement)
                math_tokens[math_element_token] = Math(
                    resolve_share_elements(tree_to_unicode(math_element))
                )
            document = [
                [
                    math_tokens[token] if token in math_tokens else Text(token)
                    for token in simple_preprocess(
                        ' '.join(paragraph.itertext()),
                        max_len=float('inf'),
                    )
                ]
                for paragraph in xml_document.xpath('//div[contains(@class, "ltx_para")]')
            ]
        return (zip_filename, filename, document)


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


def latex_tokenize(mathml_tokens):
    html5_parser = etree.HTMLParser()
    math_tree = etree.XML(mathml_tokens.encode('utf-8'), html5_parser)
    math_elements = math_tree.xpath('//math')
    assert len(math_elements) > 0
    math_element = math_elements[0]
    math_tokens = [math_element.attrib['alttext']]
    return math_tokens


def opt_tokenize(mathml_tokens):
    math_tree = MathExtractor.convert_to_semanticsymbol(mathml_tokens)
    math_tokens = [
        '\t'.join(edge)
        for edge in math_tree.get_pairs('', window=2, eob=True)
    ]
    return math_tokens


def slt_tokenize(mathml_tokens):
    math_tree = MathExtractor.convert_to_layoutsymbol(mathml_tokens)
    math_tokens = [
        '\t'.join(edge)
        for edge in math_tree.get_pairs('', window=2, eob=True)
    ]
    return math_tokens


def infix_tokenize(mathml_tokens):
    root = MathExtractor.convert_to_semanticsymbol(mathml_tokens)
    math_tokens = []
    stack = [[root, 0]]
    while stack:
        node, child_index = stack.pop()
        num_children = len(node.children or [])
        node_visited = child_index > 0
        node_completed = child_index == num_children
        if not node_visited:
            if node.tag not in TSV_OPT_INFIX_OPERATORS or num_children < 2:
                math_tokens.append(node.tag)
            if num_children > 0:
                math_tokens.append('(')
        else:
            if not node_completed:
                if node.tag not in TSV_OPT_INFIX_OPERATORS:
                    math_tokens.append(',')
                else:
                    math_tokens.append(node.tag)
            else:
                math_tokens.append(')')
        if not node_completed:
            child_node = node.children[child_index]
            stack.append((node, child_index + 1))
            stack.append((child_node, 0))
    return math_tokens


def prefix_tokenize(mathml_tokens):
    root = MathExtractor.convert_to_semanticsymbol(mathml_tokens)
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
    math_tokens = [node.tag for node in visited_list]
    return math_tokens
