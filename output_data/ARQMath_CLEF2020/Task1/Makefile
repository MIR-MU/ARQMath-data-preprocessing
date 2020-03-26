.PHONY: all

RUN_SCRIPT=cd ../../.. && python3 -m

CMML=Formula_topics_cmml.V1.2.failures Formula_topics_cmml.V1.2.tsv
PMML=Formula_topics_pmml.V1.2.failures Formula_topics_pmml.V1.2.tsv
OPT=Formula_topics_opt.V1.2.failures Formula_topics_opt.V1.2.tsv
SLT=Formula_topics_slt.V1.2.failures Formula_topics_slt.V1.2.tsv
PREFIX=Formula_topics_prefix.V1.2.failures Formula_topics_prefix.V1.2.tsv
INFIX=Formula_topics_infix.V1.2.failures Formula_topics_infix.V1.2.tsv

all: $(CMML) $(PMML) $(OPT) $(SLT) $(PREFIX) $(INFIX)

$(CMML) $(PMML):
	$(RUN_SCRIPT) scripts.latex_tsv_to_cmml_and_pmml_tsv test

$(OPT): $(CMML)
	$(RUN_SCRIPT) scripts.cmml_tsv_to_opt_tsv test

$(SLT): $(PMML)
	$(RUN_SCRIPT) scripts.pmml_tsv_to_slt_tsv test

$(PREFIX): $(CMML)
	$(RUN_SCRIPT) scripts.cmml_tsv_to_prefix_tsv test

$(INFIX): $(CMML)
	$(RUN_SCRIPT) scripts.cmml_tsv_to_infix_tsv test
