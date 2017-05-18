#!/usr/local/bin/python
import sys, codecs
import re, math
from nltk.util import ngrams
from optparse import OptionParser
import numpy

OUTDATAFILE="training.dat"
OUTTESTFILE="test.dat"

usage = "usage: %prog [options] -f <training_file> -t <test_file>"
parser = OptionParser(usage=usage)
parser.add_option("-f", "--file", dest="trainingfile", help="training file")
parser.add_option("-t", "--tfile", dest="testfile", help="test file")
parser.add_option("-c", "--class", type="choice", action="store", dest="mode", choices=['subj', 'pos', 'neg', 'iro'], default='subj', help='Task (for Evalita): subjectivity, polarity (positive or negative) or irony')
(options, args) = parser.parse_args()

if options.trainingfile==None or options.testfile==None:
	parser.print_help()
	sys.exit(-1)
	
features={}
f_count=1

trf=codecs.open(options.trainingfile, "r", "utf-8")
trout=codecs.open(OUTDATAFILE, "w", "utf-8")

for line in trf.xreadlines():
	elems=(line.strip()).split('\t')
	tweet_id=elems[0]
	if options.mode=='subj': label=elems[1]
	elif options.mode=='pos': label=elems[2]
	elif options.mode=='neg': label=elems[3]
	else: label=elems[4]
	#skipping thematic tag
	text=elems[6]
	tagged_text=elems[7]
	
	tokens=tagged_text.split(' ')
	
	row_features=set([])
	
	for t in tokens:
		try:
			(w, pos, lemma)=t.split('/')
		except:
			continue
		
		try:
			fID=features[lemma]
		except KeyError:
			features[lemma]=f_count
			fID=f_count
			f_count+=1
		
		row_features.add((fID, lemma))
		
	
	sfeatures=sorted(row_features, key=lambda x : x[0])
	if int(label) <> 0:
		trout.write(str(label))
	else: trout.write('-1')
	for el in sfeatures:
		trout.write(' '+str(el[0])+':1')
	trout.write('\n')
	
trf.close()
trout.close()

tsf=codecs.open(options.testfile, "r", "utf-8")
tsout=codecs.open(OUTTESTFILE, "w", "utf-8")

for line in tsf.xreadlines():
	elems=(line.strip()).split('\t')
	tweet_id=elems[0]
	if options.mode=='subj': label=elems[1]
	elif options.mode=='pos': label=elems[2]
	elif options.mode=='neg': label=elems[3]
	else: label=elems[4]
	#skipping thematic tag
	text=elems[6]
	tagged_text=elems[7]
	
	tokens=tagged_text.split(' ')
	
	row_features=set([])
	
	for t in tokens:
		try:
			(w, pos, lemma)=t.split('/')
		except:
			continue
		
		try:
			fID=features[lemma]
		except KeyError:
			pass
		
		row_features.add((fID, lemma))
		
	
	sfeatures=sorted(row_features, key=lambda x : x[0])
	if int(label) <> 0:
		tsout.write(str(label))
	else: tsout.write('-1')
	for el in sfeatures:
		tsout.write(' '+str(el[0])+':1')
	tsout.write('\n')
	
tsf.close()
tsout.close()

words=[]
for k in features.keys():
	words.append((features[k], k))

sorted_words=sorted(words, key=lambda x : x[0])

for pair in sorted_words:
	print pair[0], pair[1]	