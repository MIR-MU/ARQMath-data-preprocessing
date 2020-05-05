# -*- coding:utf-8 -*-

import csv
from copy import copy
from multiprocessing import Pool
import re
import subprocess
from zipfile import ZipFile

from bs4 import BeautifulSoup
from gensim.utils import simple_preprocess as gensim_simple_preprocess
from lxml import etree
import n2w
from tangentcft.TangentS.math_tan.math_extractor import MathExtractor
from tqdm import tqdm

from .configuration import POOL_NUM_WORKERS, POOL_CHUNKSIZE, CSV_PARAMETERS, XML_NAMESPACES, ETREE_TOSTRING_PARAMETERS, LATEXMLC, MATHMLCAN, TSV_OPT_INFIX_OPERATORS, XMLLINT, SUBPROCESS_TIMEOUT


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


def simple_preprocess(text):
    return gensim_simple_preprocess(text, max_len=float('inf'))


def ntcir_topic_read_xhtml(filename):
    with open(filename, 'rt') as f:
        xhtml_tokens = f.read()
        xml_document = unicode_to_tree(mathmlcan(xhtml_tokens))
    for topic_element in xml_document.xpath('//ntcir-math:topic | //mathml:topic', namespaces=XML_NAMESPACES):
        topic_number_elements = topic_element.xpath('.//ntcir-math:num | .//mathml:num', namespaces=XML_NAMESPACES)
        assert len(topic_number_elements) == 1
        topic_number_element = topic_number_elements[0]
        topic_number = topic_number_element.text
        tokens = []
        for math_element in topic_element.xpath('.//ntcir-math:formula/mathml:math | .//mathml:formula/mathml:math', namespaces=XML_NAMESPACES):
            etree.strip_tags(math_element, '{{{}}}semantics'.format(XML_NAMESPACES['mathml']))
            math_element = remove_namespaces(copy(math_element))
            math_token = Math(tree_to_unicode(math_element))
            tokens.append(math_token)
        for keyword_element in topic_element.xpath('.//ntcir-math:keyword | .//mathml:keyword', namespaces=XML_NAMESPACES):
            tokens.append(Text(keyword_element.text))
        yield (topic_number, tokens)


def ntcir_article_read_xhtml_worker(filename):
    formulae = []
    with open(filename, 'rt') as f:
        xhtml_tokens = f.read()
        xml_document = unicode_to_tree(mathmlcan(xhtml_tokens))
        for math_element in xml_document.xpath('//xhtml:math[@id]', namespaces=XML_NAMESPACES):
            math_element = remove_namespaces(copy(math_element))
            formulae.append((math_element.attrib['id'], Math(tree_to_unicode(math_element))))
    return filename, formulae


def arqmath_post_read_html5_worker(args):
    post_id, html5_tokens = args
    xml_document = html5_unicode_to_tree(html5_tokens)
    math_tokens = {}
    for math_element_number, math_element in enumerate(xml_document.xpath('//span[@class="math-container"]')):
        math_element_token = 'math_element_{}___'.format(
            re.sub(r'\s+', '_', n2w.convert(math_element_number))
        )
        replacement = etree.Element("span")
        replacement.text = math_element_token
        if math_element.tail:
            replacement.text += ' ' + math_element.tail
        math_element.getparent().replace(math_element, replacement)
        if 'id' in math_element.attrib:
            math_element_id = int(math_element.attrib['id'])
        else:
            math_element_id = None
        math_element_text = re.sub(r'^(\$*)(.*)\1', r'\2', math_element.text or '')
        math_tokens[math_element_token] = (math_element_id, Math(math_element_text))
    document = [
        math_tokens[token] if token in math_tokens else Text(token)
        for token in simple_preprocess(' '.join(xml_document.itertext()))
    ]
    return (post_id, document)


def ntcir_article_read_html5_worker(args):
    zip_filename, filename, only_latex = args
    try:
        with ZipFile(zip_filename, 'r') as zf:
            with zf.open(filename, 'r') as f:
                if only_latex:
                    html5_parser = etree.HTMLParser(huge_tree=True)
                    xml_document = etree.parse(f, html5_parser)
                else:
                    html5_tokens = f.read().decode('utf-8')
                    xml_tokens = mathmlcan(html5_to_xhtml(html5_tokens))
                    xml_document = unicode_to_tree(xml_tokens)
        math_tokens = {}
        for math_element_number, math_element in enumerate(xml_document.xpath('//math')):
            math_element_token = 'math_element_{}___'.format(
                re.sub(r'\s+', '_', n2w.convert(math_element_number))
            )
            replacement = etree.Element("span")
            replacement.text = math_element_token
            if math_element.tail:
                replacement.text += ' ' + math_element.tail
            math_element.getparent().replace(math_element, replacement)
            math_tokens[math_element_token] = Math(tree_to_unicode(math_element))
        document = [
            [
                math_tokens[token] if token in math_tokens else Text(token)
                for token in simple_preprocess(' '.join(paragraph.itertext()))
            ]
            for paragraph in xml_document.xpath('//div[contains(@class, "ltx_para")]')
        ]
    except etree.Error as e:
        document = []
    return (zip_filename, filename, document)


def resolve_share_elements(xml_tokens):
    xml_document = BeautifulSoup(xml_tokens, 'lxml')
    for math_element in xml_document.find_all('math'):
        for share_element in math_element.find_all('share'):
            if 'href' not in share_element:
                share_element.decompose()
                continue
            assert share_element['href'].startswith('#')
            shared_element = math_element.find(id=share_element['href'][1:])
            if shared_element:
                share_element.replace_with(copy(shared_element))
            else:
                share_element.decompose()
    return str(xml_document)


def isolate_latex(tree):
    annotation_elements = tree.xpath('//*[local-name() = "annotation" and @encoding = "application/x-tex"]')
    assert len(annotation_elements) > 0, "<math> elements contains no annotation with LaTeX source code"
    annotation_element = annotation_elements[0]
    return annotation_element.text


def remove_namespaces(tree):
    for element in tree.xpath('descendant-or-self::*[namespace-uri()!=""]'):
        element.tag = etree.QName(element).localname
    etree.cleanup_namespaces(tree)
    return tree


def unicode_to_tree(text):
    xml_parser = etree.XMLParser(huge_tree=True)
    return etree.XML(text.encode(ETREE_TOSTRING_PARAMETERS['encoding']), xml_parser)


def html5_unicode_to_tree(text):
    html5_parser = etree.HTMLParser(huge_tree=True)
    return etree.XML(text.encode(ETREE_TOSTRING_PARAMETERS['encoding']), html5_parser)


def tree_to_unicode(tree):
    return etree.tostring(tree, **ETREE_TOSTRING_PARAMETERS).decode(ETREE_TOSTRING_PARAMETERS['encoding'])


def latexml(latex_input):
    return execute(LATEXMLC, latex_input)


def mathmlcan(xml_input):
    xml_input = resolve_share_elements(xml_input)
    return execute(MATHMLCAN, xml_input)


def html5_to_xhtml(html5_input):
    return execute(XMLLINT, html5_input)


def execute(command, unicode_input):
    str_input = unicode_input.encode('utf-8')
    process = subprocess.Popen(
        command,
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    try:
        str_output = process.communicate(
            str_input,
            timeout=SUBPROCESS_TIMEOUT,
        )[0]
    except TimeoutExpired as e:
        process.kill()
        raise e
    unicode_output = str_output.decode('utf-8')
    return unicode_output


def cmml_and_pmml_read_tsv_worker(row):
    document = unicode_to_tree(resolve_share_elements(row[-1]))
    math_elements = document.xpath('//mathml:math', namespaces=XML_NAMESPACES)
    if len(math_elements) > 0:
        math_element = math_elements[0]
        etree.strip_tags(math_element, '{{{}}}semantics'.format(XML_NAMESPACES['mathml']))
        math_tokens = tree_to_unicode(math_element)
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
