# ARQMath Data Preprocessing

This repository contains scripts for producting preprocessed [ARQMath
competition][ARQMath] datasets:

- `output_data/ARQMath_CLEF2020/Formulas/formula_*.V1.0.{tsv,failures}`  
  all formulae for the [ARQMath competition][ARQMath],
- `output_data/ARQMath_CLEF2020/Task1/Sample Topics/Formula_topics_*_V2.0.{tsv,failures}`  
  formulae from sample topics for task 1 of the [ARQMath competition][ARQMath],
- `output_data/ARQMath_CLEF2020/Task1/Topics/Formula_topics_*_V2.0.{tsv,failures}`  
  formulae from testing topics for task 1 of the [ARQMath competition][ARQMath],
- `output_data/ARQMath_CLEF2020/Task2/Formula_topics_*_V2.0.{tsv,failures}`  
  formulae from testing topics for task 2 of the [ARQMath competition][ARQMath],
- `output_data/ARQMath_CLEF2020/Collection/votes-qrels.V1.0.tsv`  
  our relevance judgements for task 1 of the [ARQMath competition][ARQMath],
- `output_data/ARQMath_CLEF2020/Collection/Posts_V1_0_*.json.gz`  
  the document collection for the [ARQMath competition][ARQMath],
- `output_data/arxiv-dataset-arXMLiv-08-2019/arxmliv_*_08_2019_*.json.gz.{json.gz,failures}`  
  tokenized documents and paragraphs from the [arXMLiv 08.2019 dataset][arXMLiv],
- `output_data/ntcir/NTCIR11-Math/NTCIR11-Math2-queries-*-participants.{json,failures}`  
  tokenized topics from the [NTCIR-11 Math-2 Task Main Subtask][ntcir-11-math-2], and
- `output_data/ntcir/NTCIR12-Math/NTCIR12-Math-queries-*-participants.{json,failures}`  
  tokenized topics from the [NTCIR-12 MathIR Task ArXiv Main Subtask][ntcir-12-mathir].
- `output_data/ntcir/NTCIR12-Math-Wiki-Formula/NTCIR12-MathWikiFormula-queries-*-participants.{json,failures}`  
  tokenized topics from the [NTCIR-12 MathIR Task MathWikiFormula Subtask][ntcir-12-mathir].
- `output_data/ntcir/NTCIR12-Math-Wiki-Formula/MathTagArticles_*.json.gz`  
  tokenized arXiv articles from the [NTCIR-12 MathIR Task MathWikiFormula Subtask][ntcir-12-mathir].

## Downloading the preprocessed datasets

To download the preprocessed datasets, run the following commands:

```sh
$ pip install -r requirements.txt
$ dvc pull
```

## Producing the preprocessed datasets

To produce the preprocessed datasets yourself,

- install [LaTeXML version 0.8.4][latexml],
- install [MathMLCan branch `arqmath`][mathmlcan],
- install [xmllint version 20904 ][xmllint],
- update paths for MathMLCan and for the input datasets in `scripts/configuration.py`,
- run the following commands:
    ```sh
    $ pip install -r requirements.txt
    $ dvc repro
    ```

 [arqmath]:         https://www.cs.rit.edu/~dprl/ARQMath/ (Answer Retrieval for Questions on Math)
 [arxmliv]:         https://sigmathling.kwarc.info/resources/arxmliv-dataset-082019/ (arXMLiv 08.2019 – An HTML5 dataset for arXiv.org)
 [latexml]:         https://dlmf.nist.gov/LaTeXML/ (LaTeXML: A LaTeX to XML/HTML/MathML Converter)
 [mathmlcan]:       https://github.com/MIR-MU/MathMLCan/tree/arqmath (MathMLCan – Canonicalization of different MathML encodings of equivalent formulae)
 [ntcir-11-math-2]: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.686.444&rep=rep1&type=pdf (NTCIR-11 Math-2 Task Overview)
 [ntcir-12-mathir]: https://www.cs.rit.edu/~rlaz/files/ntcir12-mathir.pdf (NTCIR-12 MathIR Task Overview)
 [xmllint]:         http://xmlsoft.org/xmllint.html (xmllint — command line XML tool)
