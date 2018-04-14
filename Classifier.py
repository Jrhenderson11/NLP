import math
import sys

# This file contains code for training a simple classifier
# it is based off (pretty much a translation of) the pseudocode given by Phil on the module canvas page  

#given class and return lists of docs

#training docs = (docname, class, ProcesedEmail)	
#classes is set of classes

#word is a word
#docs is list of docnames
def count_words_in_docs(word, docs):
	import Code
	total=0
	#print "docs; " + str(docs)

	for doc in docs:
		text = Code.get_text(doc)
		total += text.count(word)
		#print "sum" + str(total)
	return total

def total_words_in_docs(docs):
	import Code
	total=0
	#print "docs; " + str(docs)

	for doc in docs:
		email = Code.ProcessedEmail(Code.get_text(doc))
		total += len(Code.get_vocab(email))
		#print "sum" + str(total)
	return total

def train(trainingdocs, classes):
	import Code
	print "Beginning training"
	vocab = set()
	docs = []
	bigdoc = []
	logprior = {}
	loglikelihood ={}
	for item in trainingdocs:
		docname = item[0]
		doctext = Code.get_text(docname)
		email = Code.ProcessedEmail(doctext)
		#get vocab
		#V <- set of words in docs
		vocab = vocab | (Code.get_vocab(email))

	print "VOCAB CREATED"
	#Nd =number of docs
	Nd = len(trainingdocs) 

	for c in classes:
		bigdoc = Code.get_docs_in_class(c, trainingdocs)

		#Nc = number of docs from D in c 
		Nc = len(bigdoc)
		
		#calc prior
		logprior[c] = math.log(Nc / float(Nd))
		#print(logprior[c])

		total=total_words_in_docs(bigdoc)

		#bigdoc[c] <- append d for d EE D with class c
		#bigdoc = Code.getdocsinclass(str(c), docs) 
		#print "BIG"
		#print bigdoc
		i=0
		for word in vocab:
			i = i+1
			percent = float(float(i) / len(vocab)) * 100
			#print "class: " + str(c)
			#print "word " + str(i) + "/" + str(len(vocab))
			
	#		print str(float(int(percent*10))/10)+"%"

			countwc = count_words_in_docs(word, bigdoc)
			
			x = float(countwc + 1)
			y = float((total + len(vocab)))
			loglikelihood[word, c] = math.log(x/y)
	
	#ENABLE THIS TO GET GOOD IDEA OF ASSOCIATION OF WORDS AND CLASSES
	#print "likelihoods:"
	#for word in loglikelihood: 
	#	print str(word) + ": " + str(loglikelihood[word])
	
	return (logprior, loglikelihood, vocab)

def classify(testdoc, logprior, loglikelihood, classes, vocab):
	import Code
	total = {}
	for c in classes:
		total[c] = logprior[c]
		text = Code.get_text(testdoc)
		email = Code.ProcessedEmail(text)
		for word in Code.get_vocab(email):
			if word in vocab:
				total[c] = total[c] + loglikelihood[word,c]
				#return key associated with max v

	maximum= -sys.maxint -1
	bestclass = ""
	for (k, v) in total.items():
		if (v>maximum): 
			maximum = v
			bestclass = k
	return bestclass #+ " " +str(maximum)



	#for c in list(classes):
	#	print c	
	#now do training step for every class and every document
	#(logprior, loglikelihood, vocab) = Classifier.train(docs, list(classes))

	#for prior in logprior:
	#	print "prior "+prior+": " + str(logprior[prior])

	#classdict = {}

	#for i in range (0, len(fileList)):
	#		fileName = fileList[i]
	#		classification = str(Classifier.classify(fileName, logprior, loglikelihood, classes, vocab))
	#		classdict[fileName] = classification
			#print "classifying " + fileName + ": " + classification + " prior: " + str(logprior[classification.split(" ")[0]])
	#logprior, loglikelihood, classes, vocab):
	#test_classification(classdict)
