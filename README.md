# Sentiment Analysis Course

In this repository you will find material for the practical part of the Sentiment Analysis course.

The repository is organized into the following subdirectories:

* code : contains some tools to carry out basic tasks, like transforming a text into a bag-of-words representation
* data : contains the datasets in Italian ([SENTIPOLC 2014](http://www.di.unito.it/~tutreeb/sentipolc-evalita14/)) and in English ([SemEval 2015 task 11](http://alt.qcri.org/semeval2015/task11/))
* resources: contains some sentiment lexicons, in English and Italian, plus a dictionary of emojis and smileys

**Student homework:**

* a) Using [Weka](http://www.cs.waikato.ac.nz/ml/weka/downloading.html) and the basicAnalyzer.py script, do the SENTIPOLC polarity classification task, for the positive class and the negative class. Report the accuracy obtained using different classification methods (for instance, nu-SVM). Find out which words are the most discriminant, using the infogain attribute selection method.
* b) Again using Weka but the dictAnalyzer.py script, do the SENTIPOLC polarity classification task, positive and negative. Check whether the accuracy improved or not in comparison with the bag-of-words (basicAnalyzer.py) result obtained for exercice a). Find out which dictionary-based feature was the most useful (knowing that feature #1 is the sum of SentiWordNet positive scores, #2 is the sum of SentiWordNet negative scores, #3 is the sum of AFINN scores and #4 is the sum of labMT scores). 
* c) For those with Python programming skills: try to modify the dictionary-based features (for instance, average instead of sum) and repeat the tests at point b).
