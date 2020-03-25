.PHONY: all

RUN_SCRIPT=cd ../../.. && python3 -m

OPT=arxmliv_opt_08_2019.json.gz arxmliv_opt_08_2019.failures
SLT=arxmliv_slt_08_2019.json.gz arxmliv_slt_08_2019.failures
PREFIX=arxmliv_prefix_08_2019.json.gz arxmliv_prefix_08_2019.failures
INFIX=arxmliv_infix_08_2019.json.gz arxmliv_infix_08_2019.failures

all: $(OPT) $(SLT) $(PREFIX) $(INFIX)

$(OPT):
	$(RUN_SCRIPT) scripts.xhtml_to_opt_tsv

$(SLT):
	$(RUN_SCRIPT) scripts.xhtml_to_slt_tsv

$(PREFIX):
	$(RUN_SCRIPT) scripts.xhtml_to_prefix_tsv

$(INFIX):
	$(RUN_SCRIPT) scripts.xhtml_to_infix_tsv
