.PHONY: all

RUN_SCRIPT=cd ../../.. && python3 -m

OPT=NTCIR11-Math2-queries-opt-participants.json NTCIR11-Math2-queries-opt-participants.failures
SLT=NTCIR11-Math2-queries-slt-participants.json NTCIR11-Math2-queries-slt-participants.failures
PREFIX=NTCIR11-Math2-queries-prefix-participants.json NTCIR11-Math2-queries-prefix-participants.failures
INFIX=NTCIR11-Math2-queries-infix-participants.json NTCIR11-Math2-queries-infix-participants.failures
LATEX=NTCIR11-Math2-queries-latex-participants.json NTCIR11-Math2-queries-latex-participants.failures

all: $(OPT) $(SLT) $(PREFIX) $(INFIX) $(LATEX)

$(OPT):
	$(RUN_SCRIPT) scripts.xhtml_to_opt_json ntcir-11-math-2-main

$(SLT):
	$(RUN_SCRIPT) scripts.xhtml_to_slt_json ntcir-11-math-2-main

$(PREFIX):
	$(RUN_SCRIPT) scripts.xhtml_to_prefix_json ntcir-11-math-2-main

$(INFIX):
	$(RUN_SCRIPT) scripts.xhtml_to_infix_json ntcir-11-math-2-main

$(LATEX):
	$(RUN_SCRIPT) scripts.xhtml_to_latex_json ntcir-11-math-2-main
