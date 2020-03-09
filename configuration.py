import csv
import ctypes


CSV_PARAMETERS = {
    'delimiter': '\t',
    'quotechar': '"',
    'quoting': csv.QUOTE_MINIMAL,
}
csv.field_size_limit(int(ctypes.c_ulong(-1).value // 2))

TSV_ZIP_FILENAME = '/mnt/storage/ARQMath_CLEF2020/Formulas/MathML.zip'
TSV_CMML_ZIP_FILENAME = TSV_ZIP_FILENAME
TSV_PMML_ZIP_FILENAME = TSV_ZIP_FILENAME
TSV_CMML_FILENAME = 'formula_file_opt.tsv'
TSV_PMML_FILENAME = 'formula_file_slt.tsv'
TSV_OPT_FILENAME = 'output_data/ARQMath_CLEF2020/Formulas/formula_opt.V0.2.tsv'
TSV_OPT_FAILURES_FILENAME = 'output_data/ARQMath_CLEF2020/Formulas/formula_opt.V0.2.failures'
TSV_SLT_FILENAME = 'output_data/ARQMath_CLEF2020/Formulas/formula_slt.V0.2.tsv'
TSV_SLT_FAILURES_FILENAME = 'output_data/ARQMath_CLEF2020/Formulas/formula_slt.V0.2.failures'
TSV_PREFIX_FILENAME = 'output_data/ARQMath_CLEF2020/Formulas/formula_prefix.V0.2.tsv'
TSV_PREFIX_FAILURES_FILENAME = 'output_data/ARQMath_CLEF2020/Formulas/formula_prefix.V0.2.failures'

TSV_CMML_NUM_ROWS = 22868569
TSV_PMML_NUM_ROWS = 23941414

POOL_CHUNKSIZE = 1
