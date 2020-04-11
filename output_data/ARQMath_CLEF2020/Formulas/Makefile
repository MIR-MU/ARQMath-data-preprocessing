.PHONY: all sanity-check

RUN_SCRIPT=cd ../../.. && python3 -m

CMML=formula_cmml.V0.2.tsv
PMML=formula_pmml.V0.2.tsv
OPT=formula_opt.V0.2.tsv
SLT=formula_slt.V0.2.tsv
PREFIX=formula_prefix.V0.2.tsv
INFIX=formula_infix.V0.2.tsv

sanity-check:
	grep -P '^14047452\t' $(CMML)   | grep -q '<cn [^>]*>3'
	grep -P '^14047452\t' $(PMML)   | grep -q '<mn [^>]*>3'
	grep -P '^14047452\t' $(OPT)    | grep -q 'N!3'
	grep -P '^14047452\t' $(SLT)    | grep -q 'N!3'
	grep -P '^14047452\t' $(PREFIX) | grep -q 'N!3'
	grep -P '^14047452\t' $(INFIX)  | grep -q 'N!3'

all: $(CMML) $(PMML) $(OPT) $(SLT) $(PREFIX) $(INFIX)

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
