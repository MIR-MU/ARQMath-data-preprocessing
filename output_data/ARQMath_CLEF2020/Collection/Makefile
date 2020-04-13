.PHONY: all

RUN_SCRIPT=cd ../../.. && python3 -m

all: votes-qrels.V1.0.tsv

votes-qrels.V1.0.tsv:
	$(RUN_SCRIPT) scripts.xml_to_qrels_tsv
