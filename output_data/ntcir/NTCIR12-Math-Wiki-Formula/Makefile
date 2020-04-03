.PHONY: all

RUN_SCRIPT=cd ../../.. && python3 -m

OPT_TOPICS=NTCIR12-MathWikiFormula-queries-opt-participants.json
SLT_TOPICS=NTCIR12-MathWikiFormula-queries-slt-participants.json
PREFIX_TOPICS=NTCIR12-MathWikiFormula-queries-prefix-participants.json
INFIX_TOPICS=NTCIR12-MathWikiFormula-queries-infix-participants.json
LATEX_TOPICS=NTCIR12-MathWikiFormula-queries-latex-participants.json

OPT_DATA=MathTagArticles_opt.json.gz
SLT_DATA=MathTagArticles_slt.json.gz
PREFIX_DATA=MathTagArticles_prefix.json.gz
INFIX_DATA=MathTagArticles_infix.json.gz
LATEX_DATA=MathTagArticles_latex.json.gz

OPT=$(OPT_TOPICS) $(OPT_DATA)
SLT=$(SLT_TOPICS) $(SLT_DATA)
PREFIX=$(PREFIX_TOPICS) $(PREFIX_DATA)
INFIX=$(INFIX_TOPICS) $(INFIX_DATA)
LATEX=$(LATEX_TOPICS) $(LATEX_DATA)

all: $(OPT) $(SLT) $(PREFIX) $(INFIX) $(LATEX)

$(OPT_TOPICS):
	$(RUN_SCRIPT) scripts.xhtml_to_opt_json ntcir-12-mathir-math-wiki-formula

$(SLT_TOPICS):
	$(RUN_SCRIPT) scripts.xhtml_to_slt_json ntcir-12-mathir-math-wiki-formula

$(PREFIX_TOPICS):
	$(RUN_SCRIPT) scripts.xhtml_to_prefix_json ntcir-12-mathir-math-wiki-formula

$(INFIX_TOPICS):
	$(RUN_SCRIPT) scripts.xhtml_to_infix_json ntcir-12-mathir-math-wiki-formula

$(LATEX_TOPICS):
	$(RUN_SCRIPT) scripts.xhtml_to_latex_json ntcir-12-mathir-math-wiki-formula

$(OPT_DATA):
	$(RUN_SCRIPT) scripts.xhtmls_to_opt_json

$(SLT_DATA):
	$(RUN_SCRIPT) scripts.xhtmls_to_slt_json

$(PREFIX_DATA):
	$(RUN_SCRIPT) scripts.xhtmls_to_prefix_json

$(INFIX_DATA):
	$(RUN_SCRIPT) scripts.xhtmls_to_infix_json

$(LATEX_DATA):
	$(RUN_SCRIPT) scripts.xhtmls_to_latex_json
