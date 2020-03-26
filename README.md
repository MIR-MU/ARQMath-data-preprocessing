# ARQMath Data Preprocessing

This repository contains scripts for producting preprocessed [ARQMath
competition][ARQMath] datasets:

- `output_data/ARQMath_CLEF2020/Formulas/formula_*.V0.2.{tsv,failures}` – The training set of formulae for the [ARQMath competition][ARQMath]

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

 [arqmath]:   https://www.cs.rit.edu/~dprl/ARQMath/ (Answer Retrieval for Questions on Math)
 [mathmlcan]: https://github.com/MIR-MU/MathMLCan (MathMLCan – Canonicalization of different MathML encodings of equivalent formulae)
 [latexml]:   https://dlmf.nist.gov/LaTeXML/ (LaTeXML: A LaTeX to XML/HTML/MathML Converter)
