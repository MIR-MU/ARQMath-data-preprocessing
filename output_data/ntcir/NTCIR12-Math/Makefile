.PHONY: all

RUN_SCRIPT=cd ../../.. && python3 -m

OPT=NTCIR12-Math-queries-opt-participants.json
SLT=NTCIR12-Math-queries-slt-participants.json
PREFIX=NTCIR12-Math-queries-prefix-participants.json
INFIX=NTCIR12-Math-queries-infix-participants.json
LATEX=NTCIR12-Math-queries-latex-participants.json

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
