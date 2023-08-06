# VTEReports

Rewrite Perl code from http://iturrate.com/simpleNLP/ in Python 3.

Int J Med Inform. 2017 May;101:93-99. doi: 10.1016/j.ijmedinf.2017.02.011. Epub 2017 Feb 21.

simpleNLP.pl --> simpleNLP.py

Lingua: DxExtractor --> extractor.py

Lingua: Negex --> negex.py


findMatch is an implenmentation of horsepool algorithm taken from https://blog.csdn.net/he11ohell0/article/details/42393761
The implementation of Negex is taken from https://github.com/chapmanbe/negex/tree/master/negex.python


#Usage

from VTEReportsAnalysis import extraction

extracion('not found')


#Version 1.02

Remove NLTK