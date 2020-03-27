# -*- coding:utf-8 -*-

import csv
import ctypes
from os import cpu_count
from os.path import dirname, join

from tangentcft.TangentS.math_tan import latex_mml
from tangentcft.TangentS.math_tan.mathml import MathML


CSV_PARAMETERS = {
    'delimiter': '\t',
    'quotechar': '"',
    'quoting': csv.QUOTE_MINIMAL,
}
csv.field_size_limit(int(ctypes.c_ulong(-1).value // 2))

ARQMATH_INPUT_DATA_DIRNAME = '/mnt/storage/ARQMath_CLEF2020'
ARQMATH_OUTPUT_DATA_DIRNAME = 'output_data/ARQMath_CLEF2020'

ARQMATH_TRAIN_INPUT_DATA_DIRNAME = '{}/Formulas'.format(ARQMATH_INPUT_DATA_DIRNAME)
ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME = '{}/Formulas'.format(ARQMATH_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_ZIP_FILENAME = '{}/MathML.zip'.format(ARQMATH_TRAIN_INPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_CMML_ZIP_INPUT_FILENAME = ARQMATH_TRAIN_TSV_ZIP_FILENAME
ARQMATH_TRAIN_TSV_PMML_ZIP_INPUT_FILENAME = ARQMATH_TRAIN_TSV_ZIP_FILENAME
ARQMATH_TRAIN_TSV_CMML_INPUT_FILENAME = 'formula_file_opt.tsv'
ARQMATH_TRAIN_TSV_PMML_INPUT_FILENAME = 'formula_file_slt.tsv'
ARQMATH_TRAIN_TSV_CMML_OUTPUT_FILENAME = '{}/formula_cmml.V0.2.tsv'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_CMML_OUTPUT_FAILURES_FILENAME = '{}/formula_cmml.V0.2.failures'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_PMML_OUTPUT_FILENAME = '{}/formula_pmml.V0.2.tsv'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_PMML_OUTPUT_FAILURES_FILENAME = '{}/formula_pmml.V0.2.failures'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_LATEX_FILENAME = '{}/formula_latex.V0.2.tsv'.format(ARQMATH_TRAIN_INPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_OPT_FILENAME = '{}/formula_opt.V0.2.tsv'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_OPT_FAILURES_FILENAME = '{}/formula_opt.V0.2.failures'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_SLT_FILENAME = '{}/formula_slt.V0.2.tsv'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_SLT_FAILURES_FILENAME = '{}/formula_slt.V0.2.failures'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_PREFIX_FILENAME = '{}/formula_prefix.V0.2.tsv'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_PREFIX_FAILURES_FILENAME = '{}/formula_prefix.V0.2.failures'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_INFIX_FILENAME = '{}/formula_infix.V0.2.tsv'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_INFIX_FAILURES_FILENAME = '{}/formula_infix.V0.2.failures'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)

ARQMATH_TRAIN_TSV_LATEX_NUM_ROWS = 25530085
ARQMATH_TRAIN_TSV_CMML_INPUT_NUM_ROWS = 22868569
ARQMATH_TRAIN_TSV_PMML_INPUT_NUM_ROWS = 23941414
ARQMATH_TRAIN_TSV_CMML_OUTPUT_NUM_ROWS = 24572932
ARQMATH_TRAIN_TSV_PMML_OUTPUT_NUM_ROWS = 24950034
ARQMATH_TRAIN_TSV_OPT_NUM_ROWS = 24276231
ARQMATH_TRAIN_TSV_SLT_NUM_ROWS = 24950054
ARQMATH_TRAIN_TSV_PREFIX_NUM_ROWS = 24276231
ARQMATH_TRAIN_TSV_INFIX_NUM_ROWS = 24276231

ARQMATH_TEST_INPUT_DATA_DIRNAME = '{}/Task1'.format(ARQMATH_INPUT_DATA_DIRNAME)
ARQMATH_TEST_OUTPUT_DATA_DIRNAME = '{}/Task1'.format(ARQMATH_OUTPUT_DATA_DIRNAME)
ARQMATH_TEST_TSV_CMML_INPUT_FILENAME = '{}/Formula_topics_opt_V1.2.tsv'.format(ARQMATH_TEST_INPUT_DATA_DIRNAME)
ARQMATH_TEST_TSV_PMML_INPUT_FILENAME = '{}/Formula_topics_slt_V1.2.tsv'.format(ARQMATH_TEST_INPUT_DATA_DIRNAME)
ARQMATH_TEST_TSV_CMML_OUTPUT_FILENAME = '{}/Formula_topics_cmml_V1.2.tsv'.format(ARQMATH_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TEST_TSV_CMML_OUTPUT_FAILURES_FILENAME = '{}/Formula_topics_cmml_V1.2.failures'.format(ARQMATH_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TEST_TSV_PMML_OUTPUT_FILENAME = '{}/Formula_topics_pmml_V1.2.tsv'.format(ARQMATH_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TEST_TSV_PMML_OUTPUT_FAILURES_FILENAME = '{}/Formula_topics_pmml_V1.2.failures'.format(ARQMATH_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TEST_TSV_LATEX_FILENAME = '{}/Formula_topics_latex_V1.2.tsv'.format(ARQMATH_TEST_INPUT_DATA_DIRNAME)
ARQMATH_TEST_TSV_OPT_FILENAME = '{}/Formula_topics_opt_V1.2.tsv'.format(ARQMATH_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TEST_TSV_OPT_FAILURES_FILENAME = '{}/Formula_topics_opt_V1.2.failures'.format(ARQMATH_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TEST_TSV_SLT_FILENAME = '{}/Formula_topics_slt_V1.2.tsv'.format(ARQMATH_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TEST_TSV_SLT_FAILURES_FILENAME = '{}/Formula_topics_slt_V1.2.failures'.format(ARQMATH_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TEST_TSV_PREFIX_FILENAME = '{}/Formula_topics_prefix_V1.2.tsv'.format(ARQMATH_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TEST_TSV_PREFIX_FAILURES_FILENAME = '{}/Formula_topics_prefix_V1.2.failures'.format(ARQMATH_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TEST_TSV_INFIX_FILENAME = '{}/Formula_topics_infix_V1.2.tsv'.format(ARQMATH_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TEST_TSV_INFIX_FAILURES_FILENAME = '{}/Formula_topics_infix_V1.2.failures'.format(ARQMATH_TEST_OUTPUT_DATA_DIRNAME)

ARQMATH_TEST_TSV_LATEX_NUM_ROWS = 1017
ARQMATH_TEST_TSV_CMML_INPUT_NUM_ROWS = 1016
ARQMATH_TEST_TSV_PMML_INPUT_NUM_ROWS = 1016
ARQMATH_TEST_TSV_CMML_OUTPUT_NUM_ROWS = 931
ARQMATH_TEST_TSV_PMML_OUTPUT_NUM_ROWS = 955
ARQMATH_TEST_TSV_OPT_NUM_ROWS = 545
ARQMATH_TEST_TSV_SLT_NUM_ROWS = 953
ARQMATH_TEST_TSV_PREFIX_NUM_ROWS = 545
ARQMATH_TEST_TSV_INFIX_NUM_ROWS = 545

ARXMLIV_INPUT_DATA_DIRNAME = '/mnt/storage/arxiv-dataset-arXMLiv-08-2019'
ARXMLIV_OUTPUT_DATA_DIRNAME = 'output_data/arxiv-dataset-arXMLiv-08-2019'

ARXMLIV_NOPROBLEM_XHTML_ZIP_FILENAME = '{}/arxmliv_08_2019_no_problem.zip'.format(ARXMLIV_INPUT_DATA_DIRNAME)
ARXMLIV_NOPROBLEM_JSON_OPT_FILENAME = '{}/arxmliv_opt_08_2019_no_problem.json.gz'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_NOPROBLEM_JSON_OPT_FAILURES_FILENAME = '{}/arxmliv_opt_08_2019_no_problem.failures'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_NOPROBLEM_JSON_SLT_FILENAME = '{}/arxmliv_slt_08_2019_no_problem.json.gz'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_NOPROBLEM_JSON_SLT_FAILURES_FILENAME = '{}/arxmliv_slt_08_2019_no_problem.failures'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_NOPROBLEM_JSON_PREFIX_FILENAME = '{}/arxmliv_prefix_08_2019_no_problem.json.gz'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_NOPROBLEM_JSON_PREFIX_FAILURES_FILENAME = '{}/arxmliv_prefix_08_2019_no_problem.failures'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_NOPROBLEM_JSON_INFIX_FILENAME = '{}/arxmliv_infix_08_2019_no_problem.json.gz'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_NOPROBLEM_JSON_INFIX_FAILURES_FILENAME = '{}/arxmliv_infix_08_2019_no_problem.failures'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_NOPROBLEM_JSON_LATEX_FILENAME = '{}/arxmliv_latex_08_2019_no_problem.json.gz'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_NOPROBLEM_JSON_LATEX_FAILURES_FILENAME = '{}/arxmliv_latex_08_2019_no_problem.failures'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_NOPROBLEM_XHTML_NUM_DOCUMENTS = 150701

ARXMLIV_WARNING1_XHTML_ZIP_FILENAME = '{}/arxmliv_08_2019_warning_1.zip'.format(ARXMLIV_INPUT_DATA_DIRNAME)
ARXMLIV_WARNING1_JSON_OPT_FILENAME = '{}/arxmliv_opt_08_2019_warning_1.json.gz'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING1_JSON_OPT_FAILURES_FILENAME = '{}/arxmliv_opt_08_2019_warning_1.failures'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING1_JSON_SLT_FILENAME = '{}/arxmliv_slt_08_2019_warning_1.json.gz'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING1_JSON_SLT_FAILURES_FILENAME = '{}/arxmliv_slt_08_2019_warning_1.failures'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING1_JSON_PREFIX_FILENAME = '{}/arxmliv_prefix_08_2019_warning_1.json.gz'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING1_JSON_PREFIX_FAILURES_FILENAME = '{}/arxmliv_prefix_08_2019_warning_1.failures'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING1_JSON_INFIX_FILENAME = '{}/arxmliv_infix_08_2019_warning_1.json.gz'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING1_JSON_INFIX_FAILURES_FILENAME = '{}/arxmliv_infix_08_2019_warning_1.failures'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING1_JSON_LATEX_FILENAME = '{}/arxmliv_latex_08_2019_warning_1.json.gz'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING1_JSON_LATEX_FAILURES_FILENAME = '{}/arxmliv_latex_08_2019_warning_1.failures'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING1_XHTML_NUM_DOCUMENTS = 500000

ARXMLIV_WARNING2_XHTML_ZIP_FILENAME = '{}/arxmliv_08_2019_warning_2.zip'.format(ARXMLIV_INPUT_DATA_DIRNAME)
ARXMLIV_WARNING2_JSON_OPT_FILENAME = '{}/arxmliv_opt_08_2019_warning_2.json.gz'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING2_JSON_OPT_FAILURES_FILENAME = '{}/arxmliv_opt_08_2019_warning_2.failures'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING2_JSON_SLT_FILENAME = '{}/arxmliv_slt_08_2019_warning_2.json.gz'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING2_JSON_SLT_FAILURES_FILENAME = '{}/arxmliv_slt_08_2019_warning_2.failures'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING2_JSON_PREFIX_FILENAME = '{}/arxmliv_prefix_08_2019_warning_2.json.gz'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING2_JSON_PREFIX_FAILURES_FILENAME = '{}/arxmliv_prefix_08_2019_warning_2.failures'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING2_JSON_INFIX_FILENAME = '{}/arxmliv_infix_08_2019_warning_2.json.gz'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING2_JSON_INFIX_FAILURES_FILENAME = '{}/arxmliv_infix_08_2019_warning_2.failures'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING2_JSON_LATEX_FILENAME = '{}/arxmliv_latex_08_2019_warning_2.json.gz'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING2_JSON_LATEX_FAILURES_FILENAME = '{}/arxmliv_latex_08_2019_warning_2.failures'.format(ARXMLIV_OUTPUT_DATA_DIRNAME)
ARXMLIV_WARNING2_XHTML_NUM_DOCUMENTS = 328127

TSV_OPT_INFIX_OPERATORS = set(
    [
        'U!{}'.format(element[len(MathML.namespace):])
        for element in [
            MathML.approx,
            MathML.eq,
            MathML.neq,
            MathML.equivalent,
            MathML.union,
            MathML.intersect,
            MathML.plus,
            MathML.times,
            MathML._and,
            MathML._or,
        ]
    ] + [
        'O!{}'.format(element[len(MathML.namespace):])
        for element in [
            MathML.lt,
            MathML.gt,
            MathML.leq,
            MathML.geq,
            MathML.minus,
            MathML.divide,
            MathML.subset,
            MathML.prsubset,
            MathML.notsubset,
            MathML.notprsubset,
            MathML._in,
            MathML.notin,
            MathML.setdiff,
            MathML.implies,
            MathML.compose,
        ]
    ]
)

ETREE_TOSTRING_PARAMETERS = {
    'xml_declaration': True,
    'encoding': 'UTF-8',
}
XML_NAMESPACES = {
    'xhtml': 'http://www.w3.org/1999/xhtml',
    'mathml': 'http://www.w3.org/1998/Math/MathML',
}

POOL_CHUNKSIZE = 1
POOL_NUM_WORKERS = cpu_count()

LATEXMLC = [
    'latexmlc',
    '--preload=amsmath',
    '--preload=amsfonts',
    '--preload={}'.format(join(dirname(latex_mml.__file__), "mws.sty.ltxml")),
    '--profile=fragment',
    '--cmml',
    '--pmml',
    '-',
]
LATEXMLC_BATCH_SIZE = 1000

MATHMLCAN = [
    'java',
    '-jar',
    '/home/novotny/.m2/repository/cz/muni/fi/mir/mathml-canonicalizer/1.4.0/mathml-canonicalizer-1.4.0-jar-with-dependencies.jar',
    '/dev/stdin',
]
