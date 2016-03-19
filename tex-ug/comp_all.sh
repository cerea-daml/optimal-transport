#!/bin/bash

# Compile script

pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
