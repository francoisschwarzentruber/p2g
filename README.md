# p2g

This script produces a graph in the PDF format of a proof written in a simple text file. The proof can then be embedded in any LaTEX document.

## Usage

      python p2g.py sqrt2irrational.proof

outputs

![image](https://user-images.githubusercontent.com/43071857/220457199-372cfcdb-fd38-44d9-81ee-e9af4ba74939.png)


## Description

The tool relies on the following library:
- graphviz
- the LaTEX package dot2tex
