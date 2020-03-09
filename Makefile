.PHONY: all formulas

all: formulas

formulas: output_data/ARQMath_CLEF2020/Formulas/formula_prefix.V0.2.tsv

output_data/ARQMath_CLEF2020/Formulas/formula_prefix.V0.2.tsv: input_data/ARQMath_CLEF2020/Formulas/MathML.zip
	python -m cmml_tsv_to_prefix_tsv
