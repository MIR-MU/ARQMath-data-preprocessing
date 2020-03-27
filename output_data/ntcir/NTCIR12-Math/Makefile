.PHONY: all

RUN_SCRIPT=cd ../../.. && python3 -m

OPT=NTCIR12-Math2-queries-opt-participants.json NTCIR12-Math2-queries-opt-participants.failures
SLT=NTCIR12-Math2-queries-slt-participants.json NTCIR12-Math2-queries-slt-participants.failures
PREFIX=NTCIR12-Math2-queries-prefix-participants.json NTCIR12-Math2-queries-prefix-participants.failures
INFIX=NTCIR12-Math2-queries-infix-participants.json NTCIR12-Math2-queries-infix-participants.failures
LATEX=NTCIR12-Math2-queries-latex-participants.json NTCIR12-Math2-queries-latex-participants.failures

all: $(OPT) $(SLT) $(PREFIX) $(INFIX) $(LATEX)

$(OPT):
	$(RUN_SCRIPT) scripts.xhtml_to_opt_json ntcir-12-mathir-arxiv-main

$(SLT):
	$(RUN_SCRIPT) scripts.xhtml_to_slt_json ntcir-12-mathir-arxiv-main

$(PREFIX):
	$(RUN_SCRIPT) scripts.xhtml_to_prefix_json ntcir-12-mathir-arxiv-main

$(INFIX):
	$(RUN_SCRIPT) scripts.xhtml_to_infix_json ntcir-12-mathir-arxiv-main

$(LATEX):
	$(RUN_SCRIPT) scripts.xhtml_to_latex_json ntcir-12-mathir-arxiv-main
