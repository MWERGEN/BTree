# BTree operations visualization tool

This repository contains the python files creating a tool for visualizing a balanced tree. It can be used to understand the behaviour of a balanced tree with different orders (max. numbers of entries in a node).

To understand the behaviour, refer to [Ubiquitous B-tree (1979)](https://dl.acm.org/doi/pdf/10.1145/356770.356776) or [Wikipedia: B-tree](https://en.wikipedia.org/wiki/B-tree).


## Setup

You need to install the required packages (check requirements.txt) and afterwards, you can easily run the main.py file. 

For more information, check our german documentation. Just open the file 'documentation-paper.pdf'.

On *windows*, you can also run the *BTree/BTree.exe* file to launch the visualization as an executable.

---

## Usage

You can **insert**, **search** and **delete** whole numbers in the balanced tree. Additionally, you can bundle multiple operations in a csv file and perform them all at once. Please refer to the *example.csv* file. Unsupported instructions are ignored. Random numbers can be inserted as well. 

Feel free to try out different orders of the tree and multiple visualization speeds.
