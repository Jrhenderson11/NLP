import os
import re
import sys
import NER
import nltk
import Eval
import scipy
import Intro
import string
import Tagger
import Ontology
import analysis
import Locations
import Clusterer
from os import listdir
from pprint import pprint
from collections import Set
from collections import Counter
from os.path import isfile, join, dirname

#prints help text
def print_help():
	print("\n				HELP TEXT")
	print("\n	To run the program type into a terminal: 'python Code.py <files>'")
	print("	where <files> is a sequence of 0 or more filenames")
	print("	or any other indcator of a list of files (e.g ./files/*)")
	print("\n	If no files are given the program will ask for them when it begins")
	print("\n	This system needs to be run on a *NIX system with a dictionary file" )
	print("	located at /usr/share/words")
	print("	If you are running on windows then, don't.")
	print("	If you are running on mac (maybe it already has it) then it shouldn't be")
	print("	too tricky to copy that")
	print("	file over from a linux machine")
	print("\n	Please refer to the Readme for more detailed information")

#tests to see if naive bayes classification matches email type field
def test_classification(classdict):
	correct = 0
	for doc in classdict:
		if(classdict[doc] == create_train_triple(doc)[1]):
			#why python no allow correct++ :(
			correct = correct + 1
	print("correct: " + str(correct) + " / "+ str(len(classdict)))

#extracts text from file
def get_text(fname):
	file = open(fname, "r")
	text = file.read()
	file.close()
	return text

#returns a list of filenames that match a given class
def get_docs_in_class(c, docs):
	docsinc = []
	for doc in docs:
		if (doc[1]==c):
			docsinc.append(doc[0])
	return docsinc

#returns a set of all words in an email
def get_vocab(email):
	vocab = []
	for line in email.headings:
		just = Tagger.remove_tags(line)
		for x in re.findall("([A-z]\w+)", just):
			vocab.append(x)

	#GET WORDS FROM BODY
	for x in re.findall("([A-z]\w+)",Tagger.remove_tags(email.body)):
		vocab.append(x)
	
	return set(vocab)

#creates triple of filename, class, email object
def create_train_triple(fname):
	fname = fname.replace("un", "")
	file = open(fname, "r")
	text = file.read()
	file.close()
	classification = "None"
	if "Type: " in text:
		typeline = re.findall("Type:\s(.*)", text)[0]
		classification = re.findall("\s.*", typeline)[0].lstrip()
	print(fname)
	taggedtext = get_text(fname)
	return (fname, str(classification), ProcessedEmail(taggedtext))

#extracts text form email and stores in class
class ProcessedEmail(object):

	def __init__(self, text):
		self.headings = []
		#print((re.findall("([A-Z][a-z]+)+:.+(\n.+)?", text)))
		heads = re.findall("\n[A-Z][a-z]+:", (text.split('Abstract:')[0]))
		for str in (re.split("\n[A-Z][a-z]+:", (text.split('Abstract:')[0]))):
			self.headings.append(str)
		
		self.body = (text.split('Abstract:')[1])
		self.text = text

#checks to see if file has identification line at top
def is_valid_email(text):
	if (re.match("<(\d+\.){7}.+@([A-z]+\.?)+.+>", text) == None):
		print((re.findall("<(\d+\.){7}.+@([A-z]+\.?)+.+>", text)))
		print("does not have initial line")
		return False
	return True

#converts text into a processedEmail object
def process_email(text):
	email = (ProcessedEmail(text))
	Tagger.output_tagged_para(email.body)
	print(("==========================================="))
	NER.print_names_text(text)

def part_one(fileList, myList):
	#paragraph scores
	totPacc, totPprec, totPrec, totPf = 0, 0, 0, 0
	#sentence scores
	totSacc, totSprec, totSrec, totSf = 0, 0, 0, 0
	#time scores
	totTacc, totTprec, totTrec, totTf = 0, 0, 0, 0
	#name scores
	totNacc, totNprec, totNrec, totNf = 0, 0, 0, 0
	#location scores
	totLacc, totLprec, totLrec, totLf = 0, 0, 0, 0
	
	docs =[]
	classes = set()

	#because NER requires training a tagger it is best done as a 
	#batch process rather than repeatedly calling a function, 
	#therefore it is done here and the results processed later
	if (len(fileList) > 10):
		print("running NER on " + str(len(fileList)) + " files (might take a bit)")
	else:
		print("running NER")

	namesdict = NER.extract_names_files(fileList)
	numdict = {}

	for i in range (0, len(fileList)):
		untaggedfile = fileList[i]
		taggedfile = fileList[i].replace("un", "")

		text = get_text(untaggedfile)
		taggedtext = get_text(taggedfile)

		acnames = NER.collapse_names(NER.extract_tagged_names(taggedtext))
		nameset = NER.collapse_names(namesdict[fileList[i]])
		numnames = len(nameset)

		if numnames in numdict:
			numdict[numnames] = numdict[numnames] + 1
		else:
			numdict[numnames] = 1
	print(numdict )

	for i in range (0, len(fileList)):

		untaggedfile = fileList[i]
		taggedfile = testList[i]
		mytaggedfile = myList[i]

		text = get_text(untaggedfile)
		taggedtext = get_text(taggedfile)
		mytext = ""
		body = (text.split('Abstract:')[1])

		fileName = untaggedfile

		#prepare for training by adding this emails class to set
		#0 = fname, 1 = class, 2 = email
		triple = create_train_triple(taggedfile)
		docs.append(triple)
		

		print("class: " + str(triple[1]) + "\n")
		classes.add(str(triple[1]))

		print(("\n\n		information extracted from " + fileName))
		print("Topic:")
		print(Ontology.get_topic(text))
		
		#test sentence tagging
		print("tagged sentences + paragraphs:")
	 	
		#untagged = Tagger.remove_tags(body)
		paratagged = Tagger.output_tagged_para(body)
		senttagged = Tagger.output_tagged_sents(paratagged)
		#print(senttagged)

		#print(body in text)
		mytext = text.split("Abstract:")[0] + "Abstract:" + senttagged

		#evaluate
		acparas =  Tagger.extract_paragraphs(taggedtext)
		myparas =  Tagger.extract_paragraphs(mytext)
		acsents =  Tagger.extract_sentences(taggedtext)
		mysents =  Tagger.extract_sentences(mytext)

		#calculate scores and tally total
		(acc, prec, rec, f) = Eval.evaluate_generic(fileName, myparas, acparas)
		totPacc, totPprec, totPrec, totPf = (totPacc + acc, totPprec + prec, totPrec + rec, totPf + f)

		(acc, prec, rec, f) = Eval.evaluate_generic(fileName, mysents, acsents)
		totSacc, totSprec, totSrec, totSf = (totSacc + acc, totSprec + prec, totSrec + rec, totSf + f)

		#Time tagging
		print("Times found:")
		(stimes, etimes) = Tagger.output_tagged_time(mytext)
		mytext = Tagger.find_and_tag(set(stimes), "stime", mytext)
		mytext = Tagger.find_and_tag(set(etimes), "etime", mytext)
		
		acstimes = Tagger.extract_stimes(taggedtext)
		acetimes = Tagger.extract_etimes(taggedtext)

		#eval times
		(acc, prec, rec, f) = Eval.evaluate_generic(fileName, stimes, acstimes)
		totTacc, totTprec, totTrec, totTf = (totTacc + acc, totTprec + prec, totTrec + rec, totTf + f)

		(acc, prec, rec, f) = Eval.evaluate_generic(fileName, etimes, acetimes)
		totTacc, totTprec, totTrec, totTf = (totTacc + acc, totTprec + prec, totTrec + rec, totTf + f)

		names = namesdict[fileName]
		print("people")
		print(names)

		print("ACSPEAKERS: ")
		acspeakers = NER.extract_tagged_names(taggedtext) 
		print(acspeakers)

		if names != []:
			collapsednames = NER.collapse_names(names)
			#nameset = set(collapsednames)
			print(collapsednames)
			collapsednames = NER.filter_sender(collapsednames, text) 
			
			speakers = []
			if collapsednames != {}:
				speakerdict = NER.pick_speakers(collapsednames, text)
				for num in speakerdict:
					speakers.extend(collapsednames[num])

			print("SPEAKERS:")
			print(speakers)
			notspeakers = []
			for name in names:
				if not name in speakers:
					notspeakers.append(name)
			#concat not speakers into list for evaluation
			(accuracy, precision, recall, f1) = Eval.evaluate_speakers(taggedfile, speakers, notspeakers, acspeakers)
		else:
			speakers = []
			notspeakers = []

			(accuracy, precision, recall, f1) = Eval.evaluate_speakers(taggedfile, speakers, notspeakers, acspeakers)
			#x = input()

		#tag
		mytext = Tagger.find_and_tag(speakers, "speaker", mytext)
		
		#eval names
		totNacc, totNprec, totNrec, totNf = (totNacc + acc, totNprec + prec, totNrec + rec, totNf + f)

		#Location Tagging
		locations = Locations.get_all_locations(text)
		selectedlocs = Locations.pick_locations(locations, text) 

		print("Selected locations:" )
		for loc in selectedlocs:
			print("	" + loc)
		mytext = Tagger.find_and_tag(selectedlocs, "location", mytext)

		print("ACLOCS:")
		aclocs = Locations.extract_tagged_locations(taggedtext)
		for acloc in aclocs:
			print("	" + acloc)
		#notlocs
		notlocs = []
		for loc in locations:
			if not loc in selectedlocs:
				notlocs.append(loc)
		(accuracy, precision, recall, f1) = Eval.evaluate_locations(taggedfile, selectedlocs, notlocs, aclocs)	
		if precision > 1:
			raw_input()
		totLacc = totLacc + accuracy
		totLprec = totLprec + precision
		totLrec = totLrec + recall
		totLf  =totLf + f1

		print("Topic:")
		mytext = Tagger.add_ontology_tag(mytext)
		

		print("final text:" )
		print(mytext)
		print("writing to " + myList[i])
		file = open(myList[i], "w")
		file.write(mytext)
		file.close()

		if stopping:
			if (i != (len(fileList) -1)):
				print("press enter for next email:")
			else:
				print("press enter to finish")
			x = raw_input()


	print("END:")

	print("Paragraph scores:")
	print("accuracy: " + str(totPacc  / (len(fileList))))
	print("precision: " + str(totPprec  / (len(fileList))) )
	print("recall: " + str(totPrec  / (len(fileList))))
	print("f1: " + str(totPf / (len(fileList))) + "\n")

	print("Sentence scores:")
	print("accuracy: " + str(totSacc  / (len(fileList))))
	print("precision: " + str(totSprec  / (len(fileList))) )
	print("recall: " + str(totSrec  / (len(fileList))))
	print("f1: " + str(totSf / (len(fileList))) + "\n")

	print("Time scores:")
	print("accuracy: " + str(totTacc  / (2*len(fileList))))
	print("precision: " + str(totTprec  / (2*len(fileList))) )
	print("recall: " + str(totTrec  / (2*len(fileList))))
	print("f1: " + str(totTf / (2*len(fileList))) + "\n")
	
	print("NER scores:")
	print("accuracy: " + str(totNacc  / len(fileList)))
	print("precision: " + str(totNprec  / len(fileList)) )
	print("recall: " + str(totNrec  / len(fileList)))
	print("f1: " + str(totNf / len(fileList)) + "\n")
	
	print("Location scores:")
	print("accuracy: " + str(totLacc  / len(fileList)))
	print("precision: " + str(totLprec  / len(fileList)) )
	print("recall: " + str(totLrec  / len(fileList)))
	print("f1: " + str(totLf / len(fileList))  + "\n")

	print("=========================================")
	print("	Overall:")
	print("accuracy: " + str((totLacc+totPacc+totSacc+totTacc+totNacc) / (6*len(fileList))))
	print("precision: " + str((totLprec+totPprec+totSprec+totTprec+totNprec) / (6*len(fileList))) )
	print("recall: " + str((totLrec+totPrec+totSrec+totTrec+totNrec) / (6*len(fileList))))
	print("f1: " + str((totLf+totPf+totSf+totTf+totNf) / (6*len(fileList)))  + "\n")

def part_two(myList):
	print("\n Ontology stuff:")
	ontology = Ontology.Ontology()
	ontology.insert_batch(myList)

#		MAIN METHOD
if __name__ == '__main__':
	
	fileList = sys.argv
	fileList.pop(0)
	if (fileList == ["-h"]):
		print_help()
		sys.exit()

	testList = []
	for file in fileList:
		testList.append(file.replace("un", ""))
	myList = []
	for file in fileList:
		myList.append(file.replace("test_un", "my_"))

	stopping = False
	Intro.print_intro()
	mypath = os.path.dirname(os.path.realpath(__file__))

	#print("Current Directory: " + mypath)
	#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

	if (len(fileList) == 0 ):
		print(("\ninput a filename"))
		fileList = [input()]

	#print(("Files to be processed are: ") )
	#print((fileList))

	print(("----------------------------------------"))

	#matrix dict is dictionary keys=filename values=tfidf matrix
	(matrix_dict, dimensions) = analysis.generate_tfidf_matrix_batch(fileList)
	print("created tf-idf matrix of " + str(dimensions) + " dimensions for " + str(len(matrix_dict)) + " vectors")
	unsparse = []
	for vectors in matrix_dict.values():
		unsparse.append(analysis.unsparsify(vectors, dimensions))

	#Clusterer.plot_cluster_v_inertia(unsparse, 1, 200)
	#Clusterer.plot_clusters(unsparse, clust_labels, clust_cents)

	#make km model from vectors then individually predict and assign to storage (dis is leng)

	#dictionary between keys=files and values=label
	file_label_dict = dict()
	#dictionary between keys=label and values=filename
	label_file_dict = dict()

	(clust_labels, clust_cents, inertia, km_model) = Clusterer.kmeans_cluster(unsparse)
	for file in matrix_dict:
		unsparsified = analysis.unsparsify(matrix_dict[file], dimensions)
		label = km_model.predict([unsparsified])[0]
		file_label_dict[file]=label
		if label in label_file_dict:
			label_file_dict[label].append(file)
		else:
			label_file_dict[label] = [file]

	#now go through labels and collect common words
	for label in label_file_dict:
		total = ""

		for file in label_file_dict[label]:
			f = open(file, 'r')
			text = f.read()
			f.close()
			total+=" " + Ontology.get_topic(text)

	
		word_counts = Counter([word.upper() for word in total.split(" ")])
		#flip dict, sort and get out words in order, fuck this is effort
		word_counts = {v: k for k, v in word_counts.items()}
		nums = list(word_counts.keys())
		nums.reverse()
		topten = []
		for x in nums[:10]:
			topten.append(word_counts[x])
		print("topten: " + str(topten))

	#print("Centres: ")
	#pprint(clust_cents)