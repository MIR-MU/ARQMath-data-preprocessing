.PHONY: all

RUN_SCRIPT=cd ../.. && python3 -m

NOPROBLEM_OPT=arxmliv_opt_08_2019_no_problem.json.gz
NOPROBLEM_SLT=arxmliv_slt_08_2019_no_problem.json.gz
NOPROBLEM_PREFIX=arxmliv_prefix_08_2019_no_problem.json.gz
NOPROBLEM_INFIX=arxmliv_infix_08_2019_no_problem.json.gz
NOPROBLEM_LATEX=arxmliv_latex_08_2019_no_problem.json.gz

WARNING1_OPT=arxmliv_opt_08_2019_warning_1.json.gz
WARNING1_SLT=arxmliv_slt_08_2019_warning_1.json.gz
WARNING1_PREFIX=arxmliv_prefix_08_2019_warning_1.json.gz
WARNING1_INFIX=arxmliv_infix_08_2019_warning_1.json.gz
WARNING1_LATEX=arxmliv_latex_08_2019_warning_1.json.gz

WARNING2_OPT=arxmliv_opt_08_2019_warning_2.json.gz
WARNING2_SLT=arxmliv_slt_08_2019_warning_2.json.gz
WARNING2_PREFIX=arxmliv_prefix_08_2019_warning_2.json.gz
WARNING2_INFIX=arxmliv_infix_08_2019_warning_2.json.gz
WARNING2_LATEX=arxmliv_latex_08_2019_warning_2.json.gz

NOPROBLEM=$(NOPROBLEM_OPT) $(NOPROBLEM_SLT) $(NOPROBLEM_PREFIX) $(NOPROBLEM_INFIX) $(NOPROBLEM_LATEX)
WARNING1=$(WARNING1_PREFIX)
WARNING2=$(WARNING2_PREFIX)

all: $(NOPROBLEM) $(WARNING1) $(WARNING2)

$(NOPROBLEM_OPT):
	$(RUN_SCRIPT) scripts.html5s_to_opt_json no_problem

$(NOPROBLEM_SLT):
	$(RUN_SCRIPT) scripts.html5s_to_slt_json no_problem

$(NOPROBLEM_PREFIX):
	$(RUN_SCRIPT) scripts.html5s_to_prefix_json no_problem

$(NOPROBLEM_INFIX):
	$(RUN_SCRIPT) scripts.html5s_to_infix_json no_problem

$(NOPROBLEM_LATEX):
	$(RUN_SCRIPT) scripts.html5s_to_latex_json no_problem

$(WARNING1_PREFIX):
	$(RUN_SCRIPT) scripts.html5s_to_prefix_json warning_1

$(WARNING2_PREFIX):
	$(RUN_SCRIPT) scripts.html5s_to_prefix_json warning_2
