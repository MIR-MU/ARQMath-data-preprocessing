.PHONY: all sanity-check

RUN_SCRIPT=cd ../../../.. && python3 -m

NUM_LINES=$$((98 + 2))

TSV_CMML=Formula_topics_cmml.V2.0.tsv
TSV_PMML=Formula_topics_pmml.V2.0.tsv
TSV_OPT=Formula_topics_opt.V2.0.tsv
TSV_SLT=Formula_topics_slt.V2.0.tsv
TSV_PREFIX=Formula_topics_prefix.V2.0.tsv
TSV_INFIX=Formula_topics_infix.V2.0.tsv

TSV=$(TSV_CMML) $(TSV_PMML) $(TSV_OPT) $(TSV_SLT) $(TSV_PREFIX) $(TSV_INFIX)

POSTS_LATEX=Topics.V2.0_latex.json.gz
POSTS_OPT=Topics.V2.0_opt.json.gz
POSTS_SLT=Topics.V2.0_slt.json.gz
POSTS_PREFIX=Topics.V2.0_prefix.json.gz
POSTS_INFIX=Topics.V2.0_infix.json.gz

POSTS=$(POSTS_LATEX) $(POSTS_OPT) $(POSTS_SLT) $(POSTS_PREFIX) $(POSTS_INFIX)

all: $(TSV) $(POSTS)

sanity-check:
	test $$(gzip -d < $(POSTS_INFIX) | awk '{ print $$1 }' | wc -l) = $(NUM_LINES)
	gzip -d < $(POSTS_INFIX) | grep -q '^"A.1":.*"text:finding", "text:value", "text:of"'
	gzip -d < $(POSTS_INFIX) | grep -q '^"A.1":.*"text:for", "text:which", "text:the", "text:range", "text:of", "math:(", "math:V!f", "math:U!times", "math:V!x", "math:)", "text:does", "text:not", "text:contain"'
	gzip -d < $(POSTS_INFIX) | grep -q '^"A.1":.*"text:functions"]'
	test $$(gzip -d < $(POSTS_PREFIX) | awk '{ print $$1 }' | wc -l) = $(NUM_LINES)
	gzip -d < $(POSTS_PREFIX) | grep -q '^"A.1":.*"text:finding", "text:value", "text:of"'
	gzip -d < $(POSTS_PREFIX) | grep -q '^"A.1":.*"text:for", "text:which", "text:the", "text:range", "text:of", "math:U!times", "math:V!f", "math:V!x", "text:does", "text:not", "text:contain"'
	gzip -d < $(POSTS_PREFIX) | grep -q '^"A.1":.*"text:functions"]'
	test $$(gzip -d < $(POSTS_LATEX) | awk '{ print $$1 }' | wc -l) = $(NUM_LINES)
	gzip -d < $(POSTS_LATEX) | grep -q '^"A.1":.*"text:finding", "text:value", "text:of"'
	gzip -d < $(POSTS_LATEX) | grep -q '^"A.1":.*"text:for", "text:which", "text:the", "text:range", "text:of", "math:f(x)", "text:does", "text:not", "text:contain"'
	gzip -d < $(POSTS_LATEX) | grep -q '^"A.1":.*"text:functions"]'
	test $$(gzip -d < $(POSTS_OPT) | awk '{ print $$1 }' | wc -l) = $(NUM_LINES)
	gzip -d < $(POSTS_OPT) | grep -q '^"A.1":.*"text:finding", "text:value", "text:of"'
	gzip -d < $(POSTS_OPT) | grep -q '^"A.1":.*"text:for", "text:which", "text:the", "text:range", "text:of", "math:U!times\\tV!f\\t0\\t-", "math:V!f\\t0!\\t0\\t0", "math:U!times\\tV!x\\t0\\t-", "math:V!x\\t0!\\t0\\t0", "text:does", "text:not", "text:contain"'
	gzip -d < $(POSTS_OPT) | grep -q '^"A.1":.*"text:functions"]'
	test $$(gzip -d < $(POSTS_SLT) | awk '{ print $$1 }' | wc -l) = $(NUM_LINES)
	gzip -d < $(POSTS_SLT) | grep -q '^"A.1":.*"text:finding", "text:value", "text:of"'
	gzip -d < $(POSTS_SLT) | grep -q '^"A.1":.*"text:for", "text:which", "text:the", "text:range", "text:of", "math:V!f\\tM!()1x1\\tn\\t-", "math:V!f\\tV!x\\tnw\\t-", "math:M!()1x1\\tV!x\\tw\\tn", "math:V!x\\t0!\\tn\\tnw", "math:M!()1x1\\t0!\\tn\\tn", "text:does", "text:not", "text:contain"'
	gzip -d < $(POSTS_SLT) | grep -q '^"A.1":.*"text:functions"]'

$(TSV_CMML) $(TSV_PMML):
	$(RUN_SCRIPT) scripts.latex_tsv_to_cmml_and_pmml_tsv task1-test

$(TSV_OPT): $(TSV_CMML)
	$(RUN_SCRIPT) scripts.cmml_tsv_to_opt_tsv task1-test

$(TSV_SLT): $(TSV_PMML)
	$(RUN_SCRIPT) scripts.pmml_tsv_to_slt_tsv task1-test

$(TSV_PREFIX): $(TSV_CMML)
	$(RUN_SCRIPT) scripts.cmml_tsv_to_prefix_tsv task1-test

$(TSV_INFIX): $(TSV_CMML)
	$(RUN_SCRIPT) scripts.cmml_tsv_to_infix_tsv task1-test

$(POSTS_LATEX):
	$(RUN_SCRIPT) scripts.xml_and_csv_to_latex_json task1-topics

$(POSTS_OPT):
	$(RUN_SCRIPT) scripts.xml_and_csv_to_opt_json task1-topics

$(POSTS_SLT):
	$(RUN_SCRIPT) scripts.xml_and_csv_to_slt_json task1-topics

$(POSTS_PREFIX):
	$(RUN_SCRIPT) scripts.xml_and_csv_to_prefix_json task1-topics

$(POSTS_INFIX):
	$(RUN_SCRIPT) scripts.xml_and_csv_to_infix_json task1-topics
