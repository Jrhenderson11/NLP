import os
import re
import sys
import NER
import nltk
import Eval
import Intro
import string
import Tagger
import Ontology
import Locations
import Classifier
from os import listdir
from collections import Set
from collections import Counter
from os.path import isfile, join, dirname

#prints help text
def print_help():
	print "\n				HELP TEXT"
	print "\n	To run the program type into a terminal: 'python Code.py <files>'"
	print "	where <files> is a sequence of 0 or more filenames"
	print "	or any other indcator of a list of files (e.g ./files/*)"
	print "\n	If no files are given the program will ask for them when it begins"
	print "\n	This system needs to be run on a *NIX system with a dictionary file" 
	print "	located at /usr/share/words"
	print "	If you are running on windows then, don't."
	print "	If you are running on mac (maybe it already has it) then it shouldn't be"
	print "	too tricky to copy that"
	print "	file over from a linux machine"
	print "\n	Please refer to the Readme for more detailed information"

#extracts text from file
def get_text(fname):
	file = open(fname, "r")
	text = file.read()
	file.close()
	return text

#extracts text form email and stores in class
class ProcessedEmail(object):

	def __init__(self, text):
	 	self.headings = []
	 	#print (re.findall("([A-Z][a-z]+)+:.+(\n.+)?", text))
	 	heads = re.findall("\n[A-Z][a-z]+:", (text.split('Abstract:')[0]))
		for str in (re.split("\n[A-Z][a-z]+:", (text.split('Abstract:')[0]))):
			self.headings.append(str)
		
		self.body = (text.split('Abstract:')[1])
		self.text = text

#checks to see if file has identification line at top
def is_valid_email(text):
	if (re.match("<(\d+\.){7}.+@([A-z]+\.?)+.+>", text) == None):
		print (re.findall("<(\d+\.){7}.+@([A-z]+\.?)+.+>", text))
		print "does not have initial line"
		return False
	return True

#converts text into a processedEmail object
def process_email(text):
	email = (ProcessedEmail(text))
	#Tagger.output_tagged_para(email.body)
	#print ("===========================================")
	#NER.print_names_text(text)


#		MAIN METHOD
if __name__ == '__main__':

	
	fileList = sys.argv
	fileList.pop(0)
	testList = []

	for file in fileList:
		testList.append(file.replace("test_untagged", "my_tagged"))


	#fileName = fileList[0]

	if (fileList == ["-h"]):
		print_help()
		sys.exit()


	stopping = False
	Intro.print_intro()
	mypath = os.path.dirname(os.path.realpath(__file__))

	#print("Current Directory: " + mypath)
	#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

	if (len(fileList) == 0 ):
		print ("\nRunning on all test data")
		fname = input()
		fileList = [fname]

	#print ("Files to be processed are: ") 
	#print (fileList)

	print ("----------------------------------------")
	docs =[]
	classes = set()

	#because NER requires training a tagger it is best done as a 
	#batch process rather than repeatedly calling a function, 
	#therefore it is done here and the results processed later
	if (len(fileList) > 10):
		print "running NER on " + str(len(fileList)) + " files (might take a bit)"
	else:
		print "running NER"

	namesdict = NER.extract_names_files(fileList)
	numdict = {}


	for i in range (0, len(fileList)):
		untaggedfile = fileList[i]

		text = get_text(untaggedfile)


		nameset = NER.collapse_names(namesdict[fileList[i]])
		
		numnames = len(nameset)

		if numnames in numdict:
			numdict[numnames] = numdict[numnames] + 1
		else:
			numdict[numnames] = 1
	#print numdict 

	for i in range (0, len(fileList)):

		untaggedfile = fileList[i]
		text = get_text(untaggedfile)
		fileName = fileList[i]
		body = (text.split('Abstract:')[1])
		print ("\n\n		information extracted from " + fileName)
		#raw_input()
		#test sentence tagging
		print "tagged sentences + paragraphs:"
		
		untagged = Tagger.remove_tags(body)
		paratagged = Tagger.output_tagged_para(untagged)
		senttagged = Tagger.output_tagged_sents(paratagged)
		#print senttagged

		#print body in text
		text = text.split("Abstract:")[0] + "Abstract:" + senttagged
		#print text
		#raw_input()
		#UNCOMMENT TO SEE TAGGED SENTS / PARAS
		#print Tagger.output_tagged_para(senttagged)
		#print senttagged

		#print "TOPIC:"
		#Ontology.tag_topic(get_text(fileName))

		#Time tagging
		print "Times found:"
		timetagged = Tagger.output_tagged_time(text)
	
		names = namesdict[fileName]
		collapsednames = NER.collapse_names(names)
		nameset = set(collapsednames)
		collapsednames = NER.filter_sender(collapsednames, text) 
		
		speakers = []
		if collapsednames != {}:
			speakerdict = NER.pick_speakers(collapsednames, text)
			for num in speakerdict:
				speakers.extend(collapsednames[num])

		print "SPEAKERS:"
		print speakers
#		for speaker in speakers:
		text = Tagger.find_and_tag(speakers, "speaker", text)

		#Location Tagging
		print "Locations found:"
		locations = Locations.get_all_locations(text)
		for loc in locations:
			print "	" + loc
		print "Selected locations:" 

		selectedlocs = Locations.pick_locations(locations, text) 

		for loc in selectedlocs:
			print "	" + loc
		text = Tagger.find_and_tag(selectedlocs, "location", text)

		print "Topic:"
		text = Tagger.add_ontology_tag(text)
		
		print "final text:" 
		print text
		print "writing to " + testList[i]
		file = open(testList[i], "w")
		file.write(text)
		file.close()
		
		if stopping:
			if (i != (len(fileList) -1)):
				print "press enter for next email:"
			else:
				print "press enter to finish"
			x = raw_input()