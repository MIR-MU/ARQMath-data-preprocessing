.PHONY: all sanity-check

SHELL=/bin/bash

RUN_SCRIPT=cd ../../.. && python3 -m

NUM_LINES=$$((2466080 + 2))

all: votes-qrels.V1.2.tsv Posts.V1.2_latex.json.gz Posts.V1.2_opt.json.gz Posts.V1.2_slt.json.gz Posts.V1.2_prefix.json.gz Posts.V1.2_infix.json.gz

sanity-check:
	test $$(gzip -d < Posts.V1.2_latex.json.gz | awk '{ print $$1 }' | wc -l) = $(NUM_LINES)
	test $$(gzip -d < Posts.V1.2_latex.json.gz | awk '{ print $$1 }' | sort -u | wc -l) = $(NUM_LINES)
	test $$(gzip -d < Posts.V1.2_opt.json.gz | awk '{ print $$1 }' | wc -l) = $(NUM_LINES)
	test $$(gzip -d < Posts.V1.2_opt.json.gz | awk '{ print $$1 }' | sort -u | wc -l) = $(NUM_LINES)
	test $$(gzip -d < Posts.V1.2_slt.json.gz | awk '{ print $$1 }' | wc -l) = $(NUM_LINES)
	test $$(gzip -d < Posts.V1.2_slt.json.gz | awk '{ print $$1 }' | sort -u | wc -l) = $(NUM_LINES)
	test $$(gzip -d < Posts.V1.2_prefix.json.gz | awk '{ print $$1 }' | wc -l) = $(NUM_LINES)
	test $$(gzip -d < Posts.V1.2_prefix.json.gz | awk '{ print $$1 }' | sort -u | wc -l) = $(NUM_LINES)
	test $$(gzip -d < Posts.V1.2_infix.json.gz | awk '{ print $$1 }' | wc -l) = $(NUM_LINES)
	test $$(gzip -d < Posts.V1.2_infix.json.gz | awk '{ print $$1 }' | sort -u | wc -l) = $(NUM_LINES)
	gzip -d < Posts.V1.2_latex.json.gz | grep -q '^"3058136":.*"text:implies", "text:that", "math:f(-y) = -f(y)"'
	gzip -d < Posts.V1.2_opt.json.gz | grep -q '^"3058136":.*"text:implies", "text:that", "math:U!eq\\tU!times\\t0\\t-", "math:U!eq\\tV!y\\t00\\t-", "math:U!eq\\tV!f\\t00\\t-", "math:U!times\\tV!f\\t0\\t0", "math:V!f\\t0!\\t0\\t00", "math:U!times\\tV!y\\t0\\t0", "math:V!y\\t0!\\t0\\t00", "math:U!eq\\tU!times\\t0\\t-", "math:U!eq\\tV!y\\t00\\t-", "math:U!eq\\tV!f\\t00\\t-", "math:U!times\\tV!f\\t0\\t0", "math:V!f\\t0!\\t0\\t00", "math:U!times\\tV!y\\t0\\t0", "math:V!y\\t0!\\t0\\t00"'
	gzip -d < Posts.V1.2_slt.json.gz | grep -q '^"3058136":.*"text:implies", "text:that", "math:V!f\\tM!()1x1\\tn\\t-", "math:V!f\\tV!y\\tnw\\t-", "math:V!f\\t=\\tnn\\t-", "math:M!()1x1\\t=\\tn\\tn", "math:M!()1x1\\tV!f\\tnn\\tn", "math:=\\tV!f\\tn\\tnn", "math:=\\tM!()1x1\\tnn\\tnn", "math:V!f\\tM!()1x1\\tn\\tnnn", "math:V!f\\tV!y\\tnw\\tnnn", "math:M!()1x1\\tV!y\\tw\\tnnnn", "math:V!y\\t0!\\tn\\tnnnnw", "math:M!()1x1\\t0!\\tn\\tnnnn", "math:M!()1x1\\tV!y\\tw\\tn", "math:V!y\\t0!\\tn\\tnw"'
	gzip -d < Posts.V1.2_prefix.json.gz | grep -q '^"3058136":.*"text:implies", "text:that", "math:U!eq", "math:U!times", "math:V!f", "math:V!y", "math:U!times", "math:V!f", "math:V!y"'
	gzip -d < Posts.V1.2_infix.json.gz | grep -q '^"3058136":.*"text:implies", "text:that", "math:(", "math:(", "math:V!f", "math:U!times", "math:V!y", "math:)", "math:U!eq", "math:(", "math:V!f", "math:U!times", "math:V!y", "math:)", "math:)"'

votes-qrels.V1.2.tsv:
	$(RUN_SCRIPT) scripts.xml_to_qrels_tsv

Posts.V1.2_latex.json.gz:
	$(RUN_SCRIPT) scripts.xml_and_csv_to_latex_json

Posts.V1.2_opt.json.gz:
	$(RUN_SCRIPT) scripts.xml_and_csv_to_opt_json

Posts.V1.2_slt.json.gz:
	$(RUN_SCRIPT) scripts.xml_and_csv_to_slt_json

Posts.V1.2_prefix.json.gz:
	$(RUN_SCRIPT) scripts.xml_and_csv_to_prefix_json

Posts.V1.2_infix.json.gz:
	$(RUN_SCRIPT) scripts.xml_and_csv_to_infix_json
