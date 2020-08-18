#!/bin/sh

cd MatchingPennies
python3 ./graph_MP.py
cd ..

cd RockPaperScissors
python3 ./graph_RPS.py
cd ..

cd Game
python3 ./data_analytics.py
cd ..

cd FinalPaper
pdflatex ./Giotta_Final.tex
pdflatex ./Giotta_Final.tex
bibtex ./Giotta_Final
pdflatex ./Giotta_Final.tex
pdflatex ./Giotta_Final.tex
cd ..

open ./FinalPaper/Giotta_Final.pdf


