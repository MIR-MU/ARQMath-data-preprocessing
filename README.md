# ARQMath Data Preprocessing

This repository contains scripts for producting preprocessed [ARQMath
competition][ARQMath] datasets:

- `output_data/ARQMath_CLEF2020/Formulas/formula_*.V0.2.{tsv,failures}` – the training set of formulae for the [ARQMath competition][ARQMath],
- `output_data/ARQMath_CLEF2020/Task1/Formula_topics_*_V1.2.{tsv,failures}` – the test set of formulae for the [ARQMath competition][ARQMath],
- `output_data/arxiv-dataset-arXMLiv-08-2019/arxmliv_*_08_2019_*.json.gz.{json.gz,failures}` – tokenized documents and paragraphs from the [arXMLiv 08.2019 dataset][arXMLiv],
- `output_data/ntcir/NTCIR11-Math/NTCIR11-Math2-queries-*-participants.{json,failures}` – tokenized topics from the [NTCIR-11 Math-2 Task Main Subtask][ntcir-11-math-2], and
- `output_data/ntcir/NTCIR12-Math/NTCIR12-Math-queries-*-participants.{json,failures}` – tokenized topics from the [NTCIR-12 MathIR Task ArXiv Main Subtask][ntcir-12-mathir].

## Downloading the preprocessed datasets

To download the preprocessed datasets, run the following commands:

```sh
$ pip install -r requirements.txt
$ dvc pull
```

## Producing the preprocessed datasets

To produce the preprocessed datasets yourself,

- install [LaTeXML version 0.8.4][latexml],
- install [MathMLCan commit `3d66b66`][mathmlcan],
- update paths for MathMLCan and for the input datasets in `scripts/configuration.py`,
- run the following commands:
    ```sh
    $ pip install -r requirements.txt
    $ dvc repro
    ```

 [arqmath]:         https://www.cs.rit.edu/~dprl/ARQMath/ (Answer Retrieval for Questions on Math)
 [arxmliv]:         https://sigmathling.kwarc.info/resources/arxmliv-dataset-082019/ (arXMLiv 08.2019 – An HTML5 dataset for arXiv.org)
 [latexml]:         https://dlmf.nist.gov/LaTeXML/ (LaTeXML: A LaTeX to XML/HTML/MathML Converter)
 [mathmlcan]:       https://github.com/MIR-MU/MathMLCan (MathMLCan – Canonicalization of different MathML encodings of equivalent formulae)
 [ntcir-11-math-2]: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.686.444&rep=rep1&type=pdf (NTCIR-11 Math-2 Task Overview)
 [ntcir-12-mathir]: https://www.cs.rit.edu/~rlaz/files/ntcir12-mathir.pdf (NTCIR-12 MathIR Task Overview)
