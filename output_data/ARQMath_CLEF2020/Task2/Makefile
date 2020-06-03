.PHONY: all

RUN_SCRIPT=cd ../../.. && python3 -m

CMML=Formula_topics_cmml.V2.0.tsv
PMML=Formula_topics_pmml.V2.0.tsv
OPT=Formula_topics_opt.V2.0.tsv
SLT=Formula_topics_slt.V2.0.tsv
PREFIX=Formula_topics_prefix.V2.0.tsv
INFIX=Formula_topics_infix.V2.0.tsv

all: $(CMML) $(PMML) $(OPT) $(SLT) $(PREFIX) $(INFIX) topics-formula_ids-qrels.V1.1.tsv

topics-formula_ids-qrels.V1.1.tsv:
	$(RUN_SCRIPT) scripts.xml_to_qrels_tsv task2-topics-formula_ids

$(CMML) $(PMML):
	$(RUN_SCRIPT) scripts.latex_tsv_to_cmml_and_pmml_tsv task2-test

$(OPT): $(CMML)
	$(RUN_SCRIPT) scripts.cmml_tsv_to_opt_tsv task2-test

$(SLT): $(PMML)
	$(RUN_SCRIPT) scripts.pmml_tsv_to_slt_tsv task2-test

$(PREFIX): $(CMML)
	$(RUN_SCRIPT) scripts.cmml_tsv_to_prefix_tsv task2-test

$(INFIX): $(CMML)
	$(RUN_SCRIPT) scripts.cmml_tsv_to_infix_tsv task2-test
