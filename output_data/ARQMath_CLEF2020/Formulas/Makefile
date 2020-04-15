.PHONY: all sanity-check

RUN_SCRIPT=cd ../../.. && python3 -m

CMML=formula_cmml.V1.0.tsv
PMML=formula_pmml.V1.0.tsv
OPT=formula_opt.V1.0.tsv
SLT=formula_slt.V1.0.tsv
PREFIX=formula_prefix.V1.0.tsv
INFIX=formula_infix.V1.0.tsv

all: $(CMML) $(PMML) $(OPT) $(SLT) $(PREFIX) $(INFIX)

sanity-check:
	grep -P -A 1 '^14047452\t' $(CMML)   | grep -q '<ci [^>]*>S<\/ci>'
	grep -P -A 1 '^14047452\t' $(PMML)   | grep -q '<mi [^>]*>S<\/mi>'
	grep -P      '^14047452\t' $(OPT)    | grep -q 'V!S'
	grep -P      '^14047452\t' $(SLT)    | grep -q 'V!S'
	grep -P      '^14047452\t' $(PREFIX) | grep -q 'V!S'
	grep -P      '^14047452\t' $(INFIX)  | grep -q 'V!S'

$(CMML) $(PMML):
	$(RUN_SCRIPT) scripts.latex_tsv_to_cmml_and_pmml_tsv train

$(OPT): $(CMML)
	$(RUN_SCRIPT) scripts.cmml_tsv_to_opt_tsv train

$(SLT): $(PMML)
	$(RUN_SCRIPT) scripts.pmml_tsv_to_slt_tsv train

$(PREFIX): $(CMML)
	$(RUN_SCRIPT) scripts.cmml_tsv_to_prefix_tsv train

$(INFIX): $(CMML)
	$(RUN_SCRIPT) scripts.cmml_tsv_to_infix_tsv train
