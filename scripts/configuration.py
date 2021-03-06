# -*- coding:utf-8 -*-

import csv
import ctypes
from os import cpu_count
from os.path import dirname, join
import sys

from tangentcft.TangentS.math_tan import latex_mml
from tangentcft.TangentS.math_tan.mathml import MathML


CSV_PARAMETERS = {
    'delimiter': '\t',
    'quotechar': '"',
    'quoting': csv.QUOTE_MINIMAL,
}
csv.field_size_limit(int(ctypes.c_ulong(-1).value // 2))

sys.setrecursionlimit(15000)

ARQMATH_INPUT_DATA_DIRNAME = '/mnt/storage/ARQMath_CLEF2020'
ARQMATH_OUTPUT_DATA_DIRNAME = 'output_data/ARQMath_CLEF2020'

ARQMATH_COLLECTION_INPUT_DATA_DIRNAME = '{}/Collection'.format(ARQMATH_INPUT_DATA_DIRNAME)
ARQMATH_COLLECTION_OUTPUT_DATA_DIRNAME = '{}/Collection'.format(ARQMATH_OUTPUT_DATA_DIRNAME)

ARQMATH_COLLECTION_QRELS_FILENAME = '{}/votes-qrels.V1.2.tsv'.format(ARQMATH_COLLECTION_OUTPUT_DATA_DIRNAME)

ARQMATH_COLLECTION_POSTS_LATEX_FILENAME = '{}/Posts.V1.2_latex.json.gz'.format(ARQMATH_COLLECTION_OUTPUT_DATA_DIRNAME)
ARQMATH_COLLECTION_POSTS_OPT_FILENAME = '{}/Posts.V1.2_opt.json.gz'.format(ARQMATH_COLLECTION_OUTPUT_DATA_DIRNAME)
ARQMATH_COLLECTION_POSTS_SLT_FILENAME = '{}/Posts.V1.2_slt.json.gz'.format(ARQMATH_COLLECTION_OUTPUT_DATA_DIRNAME)
# ARQMATH_COLLECTION_POSTS_PREFIX_FILENAME = '{}/Posts_V1_0_prefix.json.gz'.format(ARQMATH_COLLECTION_OUTPUT_DATA_DIRNAME)
ARQMATH_COLLECTION_POSTS_PREFIX_FILENAME = '{}/Posts.V1.2_prefix.json.gz'.format(ARQMATH_COLLECTION_OUTPUT_DATA_DIRNAME)
# ARQMATH_COLLECTION_POSTS_PREFIX_FILENAME = '{}/Posts.V1.2_prefix.json.gz_only_answers'.format(ARQMATH_COLLECTION_OUTPUT_DATA_DIRNAME)
ARQMATH_COLLECTION_POSTS_INFIX_FILENAME = '{}/Posts.V1.2_infix.json.gz'.format(ARQMATH_COLLECTION_OUTPUT_DATA_DIRNAME)

# ARQMATH_COLLECTION_POSTS_NUM_DOCUMENTS = 2477487
ARQMATH_COLLECTION_POSTS_NUM_DOCUMENTS = 2466080
# ARQMATH_COLLECTION_POSTS_NUM_DOCUMENTS = 1445495

ARQMATH_TRAIN_INPUT_DATA_DIRNAME = '{}/Formulas'.format(ARQMATH_INPUT_DATA_DIRNAME)
ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME = '{}/Formulas'.format(ARQMATH_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_LATEX_ZIP_FILENAME = '{}/latex_representation.V1.0.zip'.format(ARQMATH_TRAIN_INPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_CMML_INPUT_ZIP_FILENAME = '{}/opt_representation_V1.0.zip'.format(ARQMATH_TRAIN_INPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_PMML_INPUT_ZIP_FILENAME = '{}/slt_representation_V1.0.zip'.format(ARQMATH_TRAIN_INPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_CMML_OUTPUT_FILENAME = '{}/formula_cmml.V1.0.tsv'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_CMML_OUTPUT_FAILURES_FILENAME = '{}/formula_cmml.V1.0.failures'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_PMML_OUTPUT_FILENAME = '{}/formula_pmml.V1.0.tsv'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_PMML_OUTPUT_FAILURES_FILENAME = '{}/formula_pmml.V1.0.failures'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_OPT_FILENAME = '{}/formula_opt.V1.0.tsv'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_OPT_FAILURES_FILENAME = '{}/formula_opt.V1.0.failures'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_SLT_FILENAME = '{}/formula_slt.V1.0.tsv'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_SLT_FAILURES_FILENAME = '{}/formula_slt.V1.0.failures'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_PREFIX_FILENAME = '{}/formula_prefix.V1.0.tsv'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_PREFIX_FAILURES_FILENAME = '{}/formula_prefix.V1.0.failures'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_INFIX_FILENAME = '{}/formula_infix.V1.0.tsv'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)
ARQMATH_TRAIN_TSV_INFIX_FAILURES_FILENAME = '{}/formula_infix.V1.0.failures'.format(ARQMATH_TRAIN_OUTPUT_DATA_DIRNAME)

ARQMATH_TRAIN_TSV_LATEX_NUM_FORMULAE = 28320920
ARQMATH_TRAIN_TSV_CMML_INPUT_NUM_FORMULAE = 25366913
ARQMATH_TRAIN_TSV_PMML_INPUT_NUM_FORMULAE = 26075012
ARQMATH_TRAIN_TSV_CMML_OUTPUT_NUM_FORMULAE = 26705527
ARQMATH_TRAIN_TSV_PMML_OUTPUT_NUM_FORMULAE = 27232230
ARQMATH_TRAIN_TSV_OPT_NUM_FORMULAE = 26701190
ARQMATH_TRAIN_TSV_SLT_NUM_FORMULAE = 27180635
ARQMATH_TRAIN_TSV_PREFIX_NUM_FORMULAE = 26701190
ARQMATH_TRAIN_TSV_INFIX_NUM_FORMULAE = 26701190
ARQMATH_TASK1_VALIDATION_INPUT_DATA_DIRNAME = '{}/Task1/Sample Topics'.format(ARQMATH_INPUT_DATA_DIRNAME)
ARQMATH_TASK1_VALIDATION_OUTPUT_DATA_DIRNAME = '{}/Task1/Sample Topics'.format(ARQMATH_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_VALIDATION_TSV_CMML_INPUT_FILENAME = '{}/Formula_topics_opt_V2.0.tsv'.format(ARQMATH_TASK1_VALIDATION_INPUT_DATA_DIRNAME)
ARQMATH_TASK1_VALIDATION_TSV_PMML_INPUT_FILENAME = '{}/Formula_topics_slt_V2.0.tsv'.format(ARQMATH_TASK1_VALIDATION_INPUT_DATA_DIRNAME)
ARQMATH_TASK1_VALIDATION_TSV_CMML_OUTPUT_FILENAME = '{}/Formula_topics_cmml_V2.0.tsv'.format(ARQMATH_TASK1_VALIDATION_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_VALIDATION_TSV_CMML_OUTPUT_FAILURES_FILENAME = '{}/Formula_topics_cmml_V2.0.failures'.format(ARQMATH_TASK1_VALIDATION_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_VALIDATION_TSV_PMML_OUTPUT_FILENAME = '{}/Formula_topics_pmml_V2.0.tsv'.format(ARQMATH_TASK1_VALIDATION_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_VALIDATION_TSV_PMML_OUTPUT_FAILURES_FILENAME = '{}/Formula_topics_pmml_V2.0.failures'.format(ARQMATH_TASK1_VALIDATION_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_VALIDATION_TSV_LATEX_FILENAME = '{}/Formula_topics_latex_V2.0.tsv'.format(ARQMATH_TASK1_VALIDATION_INPUT_DATA_DIRNAME)
ARQMATH_TASK1_VALIDATION_TSV_OPT_FILENAME = '{}/Formula_topics_opt_V2.0.tsv'.format(ARQMATH_TASK1_VALIDATION_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_VALIDATION_TSV_OPT_FAILURES_FILENAME = '{}/Formula_topics_opt_V2.0.failures'.format(ARQMATH_TASK1_VALIDATION_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_VALIDATION_TSV_SLT_FILENAME = '{}/Formula_topics_slt_V2.0.tsv'.format(ARQMATH_TASK1_VALIDATION_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_VALIDATION_TSV_SLT_FAILURES_FILENAME = '{}/Formula_topics_slt_V2.0.failures'.format(ARQMATH_TASK1_VALIDATION_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_VALIDATION_TSV_PREFIX_FILENAME = '{}/Formula_topics_prefix_V2.0.tsv'.format(ARQMATH_TASK1_VALIDATION_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_VALIDATION_TSV_PREFIX_FAILURES_FILENAME = '{}/Formula_topics_prefix_V2.0.failures'.format(ARQMATH_TASK1_VALIDATION_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_VALIDATION_TSV_INFIX_FILENAME = '{}/Formula_topics_infix_V2.0.tsv'.format(ARQMATH_TASK1_VALIDATION_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_VALIDATION_TSV_INFIX_FAILURES_FILENAME = '{}/Formula_topics_infix_V2.0.failures'.format(ARQMATH_TASK1_VALIDATION_OUTPUT_DATA_DIRNAME)

ARQMATH_TASK1_VALIDATION_TSV_LATEX_NUM_FORMULAE = 37
ARQMATH_TASK1_VALIDATION_TSV_CMML_INPUT_NUM_FORMULAE = 37
ARQMATH_TASK1_VALIDATION_TSV_PMML_INPUT_NUM_FORMULAE = 37
ARQMATH_TASK1_VALIDATION_TSV_CMML_OUTPUT_NUM_FORMULAE = 37
ARQMATH_TASK1_VALIDATION_TSV_PMML_OUTPUT_NUM_FORMULAE = 37
ARQMATH_TASK1_VALIDATION_TSV_OPT_NUM_FORMULAE = 17
ARQMATH_TASK1_VALIDATION_TSV_SLT_NUM_FORMULAE = 37
ARQMATH_TASK1_VALIDATION_TSV_PREFIX_NUM_FORMULAE = 17
ARQMATH_TASK1_VALIDATION_TSV_INFIX_NUM_FORMULAE = 17

ARQMATH_TASK1_TEST_INPUT_DATA_DIRNAME = '{}/Task1/Topics'.format(ARQMATH_INPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME = '{}/Task1/Topics'.format(ARQMATH_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_INPUT_POSTS_FILENAME = '{}/Topics_V2.0.xml'.format(ARQMATH_TASK1_TEST_INPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_TSV_CMML_INPUT_FILENAME = '{}/Formula_topics_opt_V2.0.tsv'.format(ARQMATH_TASK1_TEST_INPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_TSV_PMML_INPUT_FILENAME = '{}/Formula_topics_slt_V2.0.tsv'.format(ARQMATH_TASK1_TEST_INPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_TSV_CMML_OUTPUT_FILENAME = '{}/Formula_topics_cmml_V2.0.tsv'.format(ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_TSV_CMML_OUTPUT_FAILURES_FILENAME = '{}/Formula_topics_cmml_V2.0.failures'.format(ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_TSV_PMML_OUTPUT_FILENAME = '{}/Formula_topics_pmml_V2.0.tsv'.format(ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_TSV_PMML_OUTPUT_FAILURES_FILENAME = '{}/Formula_topics_pmml_V2.0.failures'.format(ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_TSV_LATEX_FILENAME = '{}/Formula_topics_latex_V2.0.tsv'.format(ARQMATH_TASK1_TEST_INPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_POSTS_LATEX_FILENAME = '{}/Topics.V2.0_latex.json.gz'.format(ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_TSV_OPT_FILENAME = '{}/Formula_topics_opt_V2.0.tsv'.format(ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_TSV_OPT_FAILURES_FILENAME = '{}/Formula_topics_opt_V2.0.failures'.format(ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_POSTS_OPT_FILENAME = '{}/Topics.V2.0_opt.json.gz'.format(ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_TSV_SLT_FILENAME = '{}/Formula_topics_slt_V2.0.tsv'.format(ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_TSV_SLT_FAILURES_FILENAME = '{}/Formula_topics_slt_V2.0.failures'.format(ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_POSTS_SLT_FILENAME = '{}/Topics.V2.0_slt.json.gz'.format(ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_TSV_PREFIX_FILENAME = '{}/Formula_topics_prefix_V2.0.tsv'.format(ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_TSV_PREFIX_FAILURES_FILENAME = '{}/Formula_topics_prefix_V2.0.failures'.format(ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_POSTS_PREFIX_FILENAME = '{}/Topics.V2.0_prefix.json.gz'.format(ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_TSV_INFIX_FILENAME = '{}/Formula_topics_infix_V2.0.tsv'.format(ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_TSV_INFIX_FAILURES_FILENAME = '{}/Formula_topics_infix_V2.0.failures'.format(ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK1_TEST_POSTS_INFIX_FILENAME = '{}/Topics.V2.0_infix.json.gz'.format(ARQMATH_TASK1_TEST_OUTPUT_DATA_DIRNAME)

ARQMATH_TASK1_TEST_TSV_LATEX_NUM_FORMULAE = 1008
ARQMATH_TASK1_TEST_TSV_CMML_INPUT_NUM_FORMULAE = 1007
ARQMATH_TASK1_TEST_TSV_PMML_INPUT_NUM_FORMULAE = 1007
ARQMATH_TASK1_TEST_TSV_CMML_OUTPUT_NUM_FORMULAE = 919
ARQMATH_TASK1_TEST_TSV_PMML_OUTPUT_NUM_FORMULAE = 942
ARQMATH_TASK1_TEST_TSV_OPT_NUM_FORMULAE = 919
ARQMATH_TASK1_TEST_TSV_SLT_NUM_FORMULAE = 940
ARQMATH_TASK1_TEST_TSV_PREFIX_NUM_FORMULAE = 919
ARQMATH_TASK1_TEST_TSV_INFIX_NUM_FORMULAE = 919

ARQMATH_TASK1_TEST_POSTS_NUM_DOCUMENTS = 98

ARQMATH_TASK2_TEST_INPUT_DATA_DIRNAME = '{}/Task2'.format(ARQMATH_INPUT_DATA_DIRNAME)
ARQMATH_TASK2_TEST_OUTPUT_DATA_DIRNAME = '{}/Task2'.format(ARQMATH_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK2_QRELS_FILENAME = '{}/topics-formula_ids-qrels.V1.1.tsv'.format(ARQMATH_TASK2_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK2_TEST_INPUT_POSTS_FILENAME = '{}/Topics_V1.1.xml'.format(ARQMATH_TASK2_TEST_INPUT_DATA_DIRNAME)
ARQMATH_TASK2_TEST_TSV_CMML_INPUT_FILENAME = '{}/Formula_topics_opt_V2.0.tsv'.format(ARQMATH_TASK2_TEST_INPUT_DATA_DIRNAME)
ARQMATH_TASK2_TEST_TSV_PMML_INPUT_FILENAME = '{}/Formula_topics_slt_V2.0.tsv'.format(ARQMATH_TASK2_TEST_INPUT_DATA_DIRNAME)
ARQMATH_TASK2_TEST_TSV_CMML_OUTPUT_FILENAME = '{}/Formula_topics_cmml_V2.0.tsv'.format(ARQMATH_TASK2_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK2_TEST_TSV_CMML_OUTPUT_FAILURES_FILENAME = '{}/Formula_topics_cmml_V2.0.failures'.format(ARQMATH_TASK2_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK2_TEST_TSV_PMML_OUTPUT_FILENAME = '{}/Formula_topics_pmml_V2.0.tsv'.format(ARQMATH_TASK2_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK2_TEST_TSV_PMML_OUTPUT_FAILURES_FILENAME = '{}/Formula_topics_pmml_V2.0.failures'.format(ARQMATH_TASK2_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK2_TEST_TSV_LATEX_FILENAME = '{}/Formula_topics_latex_V2.0.tsv'.format(ARQMATH_TASK2_TEST_INPUT_DATA_DIRNAME)
ARQMATH_TASK2_TEST_TSV_OPT_FILENAME = '{}/Formula_topics_opt_V2.0.tsv'.format(ARQMATH_TASK2_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK2_TEST_TSV_OPT_FAILURES_FILENAME = '{}/Formula_topics_opt_V2.0.failures'.format(ARQMATH_TASK2_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK2_TEST_TSV_SLT_FILENAME = '{}/Formula_topics_slt_V2.0.tsv'.format(ARQMATH_TASK2_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK2_TEST_TSV_SLT_FAILURES_FILENAME = '{}/Formula_topics_slt_V2.0.failures'.format(ARQMATH_TASK2_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK2_TEST_TSV_PREFIX_FILENAME = '{}/Formula_topics_prefix_V2.0.tsv'.format(ARQMATH_TASK2_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK2_TEST_TSV_PREFIX_FAILURES_FILENAME = '{}/Formula_topics_prefix_V2.0.failures'.format(ARQMATH_TASK2_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK2_TEST_TSV_INFIX_FILENAME = '{}/Formula_topics_infix_V2.0.tsv'.format(ARQMATH_TASK2_TEST_OUTPUT_DATA_DIRNAME)
ARQMATH_TASK2_TEST_TSV_INFIX_FAILURES_FILENAME = '{}/Formula_topics_infix_V2.0.failures'.format(ARQMATH_TASK2_TEST_OUTPUT_DATA_DIRNAME)

ARQMATH_TASK2_TEST_TSV_LATEX_NUM_FORMULAE = 1008
ARQMATH_TASK2_TEST_TSV_CMML_INPUT_NUM_FORMULAE = 1007
ARQMATH_TASK2_TEST_TSV_PMML_INPUT_NUM_FORMULAE = 1007
ARQMATH_TASK2_TEST_TSV_CMML_OUTPUT_NUM_FORMULAE = 919
ARQMATH_TASK2_TEST_TSV_PMML_OUTPUT_NUM_FORMULAE = 942
ARQMATH_TASK2_TEST_TSV_OPT_NUM_FORMULAE = 1007
ARQMATH_TASK2_TEST_TSV_SLT_NUM_FORMULAE = 1007
ARQMATH_TASK2_TEST_TSV_PREFIX_NUM_FORMULAE = 1007
ARQMATH_TASK2_TEST_TSV_INFIX_NUM_FORMULAE = 1007

ARXMLIV_INPUT_DATA_DIRNAME = '/mnt/storage/arxiv-dataset-arXMLiv-08-2019'
ARXMLIV_OUTPUT_DATA_DIRNAME = 'output_data/arxiv-dataset-arXMLiv-08-2019'

ARXMLIV_NOPROBLEM_HTML5_ZIP_FILENAME = '{}/arxmliv_08_2019_no_problem.zip'.format(ARXMLIV_INPUT_DATA_DIRNAME)
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

ARXMLIV_NOPROBLEM_HTML5_NUM_DOCUMENTS = 150701
ARXMLIV_NOPROBLEM_HTML5_NUM_PARAGRAPHS = 5076978
ARXMLIV_NOPROBLEM_JSON_LATEX_NUM_DOCUMENTS = 136170
ARXMLIV_NOPROBLEM_JSON_SLT_NUM_DOCUMENTS = 132422
ARXMLIV_NOPROBLEM_JSON_OPT_NUM_DOCUMENTS = 150519
ARXMLIV_NOPROBLEM_JSON_PREFIX_NUM_DOCUMENTS = 150519
ARXMLIV_NOPROBLEM_JSON_INFIX_NUM_DOCUMENTS = 150519

ARXMLIV_WARNING1_HTML5_ZIP_FILENAME = '{}/arxmliv_08_2019_warning_1.zip'.format(ARXMLIV_INPUT_DATA_DIRNAME)
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

ARXMLIV_WARNING1_HTML5_NUM_DOCUMENTS = 500000
ARXMLIV_WARNING1_HTML5_NUM_PARAGRAPHS = 32761639
ARXMLIV_WARNING1_JSON_PREFIX_NUM_DOCUMENTS = 499811

ARXMLIV_WARNING2_HTML5_ZIP_FILENAME = '{}/arxmliv_08_2019_warning_2.zip'.format(ARXMLIV_INPUT_DATA_DIRNAME)
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

ARXMLIV_WARNING2_HTML5_NUM_DOCUMENTS = 328127
ARXMLIV_WARNING2_HTML5_NUM_PARAGRAPHS = 21892461

NTCIR_INPUT_DATA_DIRNAME = '/mnt/storage/ntcir'
NTCIR_OUTPUT_DATA_DIRNAME = 'output_data/ntcir'

NTCIR11_MATH2_MAIN_INPUT_DATA_DIRNAME = '{}/NTCIR11-Math'.format(NTCIR_INPUT_DATA_DIRNAME)
NTCIR11_MATH2_MAIN_OUTPUT_DATA_DIRNAME = '{}/NTCIR11-Math'.format(NTCIR_OUTPUT_DATA_DIRNAME)
NTCIR11_MATH2_MAIN_TOPICS_XHTML_FILENAME = '{}/NTCIR11-Math2-queries-participants.xml'.format(NTCIR11_MATH2_MAIN_INPUT_DATA_DIRNAME)
NTCIR11_MATH2_MAIN_TOPICS_JSON_OPT_FILENAME = '{}/NTCIR11-Math2-queries-opt-participants.json'.format(NTCIR11_MATH2_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR11_MATH2_MAIN_TOPICS_JSON_OPT_FAILURES_FILENAME = '{}/NTCIR11-Math2-queries-opt-participants.failures'.format(NTCIR11_MATH2_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR11_MATH2_MAIN_TOPICS_JSON_SLT_FILENAME = '{}/NTCIR11-Math2-queries-slt-participants.json'.format(NTCIR11_MATH2_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR11_MATH2_MAIN_TOPICS_JSON_SLT_FAILURES_FILENAME = '{}/NTCIR11-Math2-queries-slt-participants.failures'.format(NTCIR11_MATH2_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR11_MATH2_MAIN_TOPICS_JSON_PREFIX_FILENAME = '{}/NTCIR11-Math2-queries-prefix-participants.json'.format(NTCIR11_MATH2_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR11_MATH2_MAIN_TOPICS_JSON_PREFIX_FAILURES_FILENAME = '{}/NTCIR11-Math2-queries-prefix-participants.failures'.format(NTCIR11_MATH2_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR11_MATH2_MAIN_TOPICS_JSON_INFIX_FILENAME = '{}/NTCIR11-Math2-queries-infix-participants.json'.format(NTCIR11_MATH2_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR11_MATH2_MAIN_TOPICS_JSON_INFIX_FAILURES_FILENAME = '{}/NTCIR11-Math2-queries-infix-participants.failures'.format(NTCIR11_MATH2_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR11_MATH2_MAIN_TOPICS_JSON_LATEX_FILENAME = '{}/NTCIR11-Math2-queries-latex-participants.json'.format(NTCIR11_MATH2_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR11_MATH2_MAIN_TOPICS_JSON_LATEX_FAILURES_FILENAME = '{}/NTCIR11-Math2-queries-latex-participants.failures'.format(NTCIR11_MATH2_MAIN_OUTPUT_DATA_DIRNAME)

NTCIR11_MATH2_MAIN_TOPICS_XHTML_NUM_TOPICS = 50
NTCIR11_MATH2_MAIN_TOPICS_JSON_LATEX_NUM_TOPICS = 50
NTCIR11_MATH2_MAIN_TOPICS_JSON_INFIX_NUM_TOPICS = 50
NTCIR11_MATH2_MAIN_TOPICS_JSON_PREFIX_NUM_TOPICS = 50
NTCIR11_MATH2_MAIN_TOPICS_JSON_OPT_NUM_TOPICS = 50
NTCIR11_MATH2_MAIN_TOPICS_JSON_SLT_NUM_TOPICS = 50

NTCIR12_MATHIR_ARXIV_MAIN_INPUT_DATA_DIRNAME = '{}/NTCIR12-Math'.format(NTCIR_INPUT_DATA_DIRNAME)
NTCIR12_MATHIR_ARXIV_MAIN_OUTPUT_DATA_DIRNAME = '{}/NTCIR12-Math'.format(NTCIR_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_XHTML_FILENAME = '{}/NTCIR12-Math-queries-participants.xml'.format(NTCIR12_MATHIR_ARXIV_MAIN_INPUT_DATA_DIRNAME)
NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_OPT_FILENAME = '{}/NTCIR12-Math-queries-opt-participants.json'.format(NTCIR12_MATHIR_ARXIV_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_OPT_FAILURES_FILENAME = '{}/NTCIR12-Math-queries-opt-participants.failures'.format(NTCIR12_MATHIR_ARXIV_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_SLT_FILENAME = '{}/NTCIR12-Math-queries-slt-participants.json'.format(NTCIR12_MATHIR_ARXIV_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_SLT_FAILURES_FILENAME = '{}/NTCIR12-Math-queries-slt-participants.failures'.format(NTCIR12_MATHIR_ARXIV_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_PREFIX_FILENAME = '{}/NTCIR12-Math-queries-prefix-participants.json'.format(NTCIR12_MATHIR_ARXIV_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_PREFIX_FAILURES_FILENAME = '{}/NTCIR12-Math-queries-prefix-participants.failures'.format(NTCIR12_MATHIR_ARXIV_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_INFIX_FILENAME = '{}/NTCIR12-Math-queries-infix-participants.json'.format(NTCIR12_MATHIR_ARXIV_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_INFIX_FAILURES_FILENAME = '{}/NTCIR12-Math-queries-infix-participants.failures'.format(NTCIR12_MATHIR_ARXIV_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_LATEX_FILENAME = '{}/NTCIR12-Math-queries-latex-participants.json'.format(NTCIR12_MATHIR_ARXIV_MAIN_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_LATEX_FAILURES_FILENAME = '{}/NTCIR12-Math-queries-latex-participants.failures'.format(NTCIR12_MATHIR_ARXIV_MAIN_OUTPUT_DATA_DIRNAME)

NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_XHTML_NUM_TOPICS = 29
NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_LATEX_NUM_TOPICS = 29
NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_INFIX_NUM_TOPICS = 29
NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_PREFIX_NUM_TOPICS = 29
NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_OPT_NUM_TOPICS = 29
NTCIR12_MATHIR_ARXIV_MAIN_TOPICS_JSON_SLT_NUM_TOPICS = 29

NTCIR12_MATHIR_MATHWIKIFORMULA_INPUT_DATA_DIRNAME = '{}/NTCIR12-Math-Wiki-Formula'.format(NTCIR_INPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME = '{}/NTCIR12-Math-Wiki-Formula'.format(NTCIR_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_TOPICS_XHTML_FILENAME = '{}/NTCIR12-MathWikiFormula-queries-participants.xml'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_INPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_TOPICS_JSON_OPT_FILENAME = '{}/NTCIR12-MathWikiFormula-queries-opt-participants.json'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_TOPICS_JSON_OPT_FAILURES_FILENAME = '{}/NTCIR12-MathWikiFormula-queries-opt-participants.failures'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_TOPICS_JSON_SLT_FILENAME = '{}/NTCIR12-MathWikiFormula-queries-slt-participants.json'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_TOPICS_JSON_SLT_FAILURES_FILENAME = '{}/NTCIR12-MathWikiFormula-queries-slt-participants.failures'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_TOPICS_JSON_PREFIX_FILENAME = '{}/NTCIR12-MathWikiFormula-queries-prefix-participants.json'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_TOPICS_JSON_PREFIX_FAILURES_FILENAME = '{}/NTCIR12-MathWikiFormula-queries-prefix-participants.failures'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_TOPICS_JSON_INFIX_FILENAME = '{}/NTCIR12-MathWikiFormula-queries-infix-participants.json'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_TOPICS_JSON_INFIX_FAILURES_FILENAME = '{}/NTCIR12-MathWikiFormula-queries-infix-participants.failures'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_TOPICS_JSON_LATEX_FILENAME = '{}/NTCIR12-MathWikiFormula-queries-latex-participants.json'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_TOPICS_JSON_LATEX_FAILURES_FILENAME = '{}/NTCIR12-MathWikiFormula-queries-latex-participants.failures'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)

NTCIR12_MATHIR_MATHWIKIFORMULA_TOPICS_XHTML_NUM_TOPICS = 40
NTCIR12_MATHIR_MATHWIKIFORMULA_TOPICS_JSON_LATEX_NUM_TOPICS = 40
NTCIR12_MATHIR_MATHWIKIFORMULA_TOPICS_JSON_INFIX_NUM_TOPICS = 40
NTCIR12_MATHIR_MATHWIKIFORMULA_TOPICS_JSON_PREFIX_NUM_TOPICS = 40
NTCIR12_MATHIR_MATHWIKIFORMULA_TOPICS_JSON_OPT_NUM_TOPICS = 40
NTCIR12_MATHIR_MATHWIKIFORMULA_TOPICS_JSON_SLT_NUM_TOPICS = 40

NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_XHTML_GLOB = '{}/dataset/MathTagArticles/*/Articles/*.html'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_INPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_OPT_FILENAME = '{}/MathTagArticles_opt.json.gz'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_OPT_FAILURES_FILENAME = '{}/MathTagArticles_opt.failures'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_SLT_FILENAME = '{}/MathTagArticles_slt.json.gz'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_SLT_FAILURES_FILENAME = '{}/MathTagArticles_slt.failures'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_PREFIX_FILENAME = '{}/MathTagArticles_prefix.json.gz'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_PREFIX_FAILURES_FILENAME = '{}/MathTagArticles_prefix.failures'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_INFIX_FILENAME = '{}/MathTagArticles_infix.json.gz'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_INFIX_FAILURES_FILENAME = '{}/MathTagArticles_infix.failures'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_LATEX_FILENAME = '{}/MathTagArticles_latex.json.gz'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)
NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_LATEX_FAILURES_FILENAME = '{}/MathTagArticles_latex.failures'.format(NTCIR12_MATHIR_MATHWIKIFORMULA_OUTPUT_DATA_DIRNAME)

NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_XHTML_NUM_DOCUMENTS = 31839
NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_LATEX_NUM_DOCUMENTS = 31547
NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_INFIX_NUM_DOCUMENTS = 31793
NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_PREFIX_NUM_DOCUMENTS = 31793
NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_OPT_NUM_DOCUMENTS = 31793
NTCIR12_MATHIR_MATHWIKIFORMULA_DATA_JSON_SLT_NUM_DOCUMENTS = 31595

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
    'with_tail': False,
}
XML_NAMESPACES = {
    'xhtml': 'http://www.w3.org/1999/xhtml',
    'mathml': 'http://www.w3.org/1998/Math/MathML',
    'ntcir-math': 'http://ntcir-math.nii.ac.jp/',
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

XMLLINT = [
    'xmllint',
    '--html',
    '--dropdtd',
    '--xpath', '//body',
    '--xmlout',
    '/dev/stdin',
]

SUBPROCESS_TIMEOUT = 3600
