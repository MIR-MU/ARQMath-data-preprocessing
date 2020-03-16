import csv
import ctypes
from os import cpu_count
from os.path import dirname, join

from tangentcft.TangentS.math_tan import latex_mml


CSV_PARAMETERS = {
    'delimiter': '\t',
    'quotechar': '"',
    'quoting': csv.QUOTE_MINIMAL,
}
csv.field_size_limit(int(ctypes.c_ulong(-1).value // 2))

ARQMATH_INPUT_DATA_DIRNAME = '/mnt/storage/ARQMath_CLEF2020/Formulas'
ARQMATH_OUTPUT_DATA_DIRNAME = 'output_data/ARQMath_CLEF2020/Formulas'
TSV_ZIP_FILENAME = '{}/MathML.zip'.format(ARQMATH_INPUT_DATA_DIRNAME)
TSV_CMML_ZIP_INPUT_FILENAME = TSV_ZIP_FILENAME
TSV_PMML_ZIP_INPUT_FILENAME = TSV_ZIP_FILENAME
TSV_CMML_INPUT_FILENAME = 'formula_file_opt.tsv'
TSV_PMML_INPUT_FILENAME = 'formula_file_slt.tsv'
TSV_CMML_OUTPUT_FILENAME = '{}/formula_cmml.V0.2.tsv'.format(ARQMATH_OUTPUT_DATA_DIRNAME)
TSV_CMML_OUTPUT_FAILURES_FILENAME = '{}/formula_cmml.V0.2.failures'.format(ARQMATH_OUTPUT_DATA_DIRNAME)
TSV_PMML_OUTPUT_FILENAME = '{}/formula_pmml.V0.2.tsv'.format(ARQMATH_OUTPUT_DATA_DIRNAME)
TSV_PMML_OUTPUT_FAILURES_FILENAME = '{}/formula_pmml.V0.2.failures'.format(ARQMATH_OUTPUT_DATA_DIRNAME)
TSV_LATEX_FILENAME = '{}/formula_latex.V0.2.tsv'.format(ARQMATH_INPUT_DATA_DIRNAME)
TSV_OPT_FILENAME = '{}/formula_opt.V0.2.tsv'.format(ARQMATH_OUTPUT_DATA_DIRNAME)
TSV_OPT_FAILURES_FILENAME = '{}/formula_opt.V0.2.failures'.format(ARQMATH_OUTPUT_DATA_DIRNAME)
TSV_SLT_FILENAME = '{}/formula_slt.V0.2.tsv'.format(ARQMATH_OUTPUT_DATA_DIRNAME)
TSV_SLT_FAILURES_FILENAME = '{}/formula_slt.V0.2.failures'.format(ARQMATH_OUTPUT_DATA_DIRNAME)
TSV_PREFIX_FILENAME = '{}/formula_prefix.V0.2.tsv'.format(ARQMATH_OUTPUT_DATA_DIRNAME)
TSV_PREFIX_FAILURES_FILENAME = '{}/formula_prefix.V0.2.failures'.format(ARQMATH_OUTPUT_DATA_DIRNAME)
HTML_CMML_FILENAME = '{}/formula_latex.V0.2.cmml.html'.format(ARQMATH_OUTPUT_DATA_DIRNAME)
HTML_PMML_FILENAME = '{}/formula_latex.V0.2.pmml.html'.format(ARQMATH_OUTPUT_DATA_DIRNAME)

TSV_LATEX_NUM_ROWS = 25530085
TSV_CMML_INPUT_NUM_ROWS = 22868569
TSV_PMML_INPUT_NUM_ROWS = 23941414
TSV_CMML_OUTPUT_NUM_ROWS = 24573083
TSV_PMML_OUTPUT_NUM_ROWS = 24950196
TSV_OPT_NUM_ROWS = 24276306
TSV_SLT_NUM_ROWS = 24950054
TSV_PREFIX_NUM_ROWS = 24276306

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
