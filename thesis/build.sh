#!/bin/sh

DOCNAME=mscthesis

echo "pdflatex pass 1"
pdflatex -shell-escape -halt-on-error $DOCNAME.tex > /dev/null
if [ $? -ne 0 ]; then
	echo "pdflatex(1) failed"
	exit 1
fi

echo "bibtex pass"
bibtex $DOCNAME.aux > /dev/null
if [ $? -ne 0 ]; then
	echo "bibtex failed"
	exit 1
fi

echo "pdflatex pass 2"
pdflatex -shell-escape -halt-on-error $DOCNAME.tex > /dev/null
if [ $? -ne 0 ]; then
	echo "pdflatex(2) failed"
	exit 1
fi

echo "pdflatex pass 3"
pdflatex -shell-escape -halt-on-error $DOCNAME.tex > /dev/null
if [ $? -ne 0 ]; then
	echo "pdflatex(3) failed"
	exit 1
fi

echo "success"

for ext in log aux blg bbl lot lof toc; do
	rm -f $DOCNAME.$ext
done

