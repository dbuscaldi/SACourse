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
f_count=5

#loading SentiWN
sentiWN={}
try:
	swf=open("../resources/it/SentiWordNet_3.0.0_ita_sorted.txt", "r")
	for line in swf.xreadlines():
		els=(line.strip()).split('\t')
		w=els[0]
		ps=float(els[1])
		ns=float(els[2])
		sentiWN[w]=(ps, ns)
	swf.close()
except:
	print "Unable to read SentiWN files"
	sys.exit(-1)

#loading AFINN Lexicon
AFINNLex={}
try:
	af=open("../resources/it/afinn-v2.txt", "r")
	for line in af.xreadlines():
		els=(line.strip()).split('#')
		pal=els[0]
		score=int(els[1])
		AFINNLex[pal]=score
	af.close()
except:
	print "Unable to read AFINN Lexicon file"
	sys.exit(-1)

labMT={} #labMT dictionary
labmt_f= codecs.open("../resources/it/labMT-italian.txt", "r", "utf-8")
for line in labmt_f.readlines()[1:]: #skipping first line
	els=line.strip().split('\t')
	w=els[0]
	pol=float(els[1])
	labMT[w]=(pol)
labmt_f.close()

#emoticons regexp
emo_txt=[]
ef = codecs.open("../resources/emoticons/all.txt", "r", "utf-8")
for line in ef.readlines():
	e=line.strip()
	emo_txt.append(re.escape(e))
ef.close()
emo_string="("+'|'.join(emo_txt)+")"
emo_re=re.compile(emo_string)
	


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
	sentiWN_pos=[]
	sentiWN_neg=[]
	afinn_scores=[]
	labMT_scores=[]
	
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
		
		#dictionary-based features
		try:
			swns=sentiWN[lemma]
		except KeyError:
			swns=(0,0)
		sentiWN_pos.append(swns[0])
		sentiWN_neg.append(swns[0])
		
		try:
			afs=AFINNLex[lemma]
		except KeyError:
			afs=0
		afinn_scores.append(afs)
		
		try:
			lmts=labMT[w]
		except KeyError:
			lmts=0
			
		labMT_scores.append(lmts)
	
	sfeatures=sorted(row_features, key=lambda x : x[0])
	if int(label) <> 0:
		trout.write(str(label))
	else: trout.write('-1')
	trout.write(' 1:'+str(sum(sentiWN_pos)))
	trout.write(' 2:'+str(sum(sentiWN_neg)))
	trout.write(' 3:'+str(sum(afinn_scores)))
	trout.write(' 4:'+str(sum(labMT_scores)))
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
	
	#dictionary-based features
	try:
		swns=sentiWN[lemma]
	except KeyError:
		swns=(0,0)
	sentiWN_pos.append(swns[0])
	sentiWN_neg.append(swns[0])
	
	try:
		afs=AFINNLex[lemma]
	except KeyError:
		afs=0
	afinn_scores.append(afs)
	
	try:
		lmts=labMT[w]
	except KeyError:
		lmts=0
		
	labMT_scores.append(lmts)
	
	sfeatures=sorted(row_features, key=lambda x : x[0])
	if int(label) <> 0:
		tsout.write(str(label))
	else: tsout.write('-1')
	tsout.write(' 1:'+str(sum(sentiWN_pos)))
	tsout.write(' 2:'+str(sum(sentiWN_neg)))
	tsout.write(' 3:'+str(sum(afinn_scores)))
	tsout.write(' 4:'+str(sum(labMT_scores)))
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