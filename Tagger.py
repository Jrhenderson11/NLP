import os
import re
import nltk
import string
import Ontology
import nltk.data
from os import listdir
from os.path import isfile
from os.path import join, dirname
from nltk.tokenize import sent_tokenize, word_tokenize

#guess what this does
def remove_tags(text):
	return re.sub("<\/?[A-z]+>", "", text)
	#consider lines individual
	#names: ([A-Z]\w+(\s([A-Z]\w+))*)
	#places: ((([A-Z]\w+)|[0-9]+)(,?\s([A-Z]\w+))*)

#function that places <paragraph> and </paragraph> tags in text
def output_tagged_para(text):
	
	#dont count these as paras (tabbed too far out)
	#r'\s{5}.*\n'
	#r'\s{5}.*'
	#r'( {5}|\t).*\n'

	final = text
	newtext = re.sub(r'.*( {5}|\t).*\n', '\n', text)

	paras = re.findall(r'((?<=((\n))).+(\n.+)*)', newtext)

	for para in paras:
		final = string.replace(final, para[0], "<paragraph>"+para[0]+"</paragraph>")
	return final

#function that places <sentence> and </sentence> tags in text, uses punkt with some preprocessing (eg only inside paras)
def output_tagged_sents(text):

	#as the tokeniser alone is prone to false positives when tagging sentences 
	#I perform some pre-processing with regex to prevent data that is not a sentence 
	#from being tagged as such

	#only take inside paratags
	paras = re.findall(r'((?<=<paragraph>)(.*\n)*?.*(?=<\/paragraph>))', text)

	#	parts= text.split("\n\n")
	for para in paras:
		part = para[0]
		#count num lines
		#find num newlines
		numlines = len(re.findall(r'\n', part)) + 1
		
		if (numlines > 1 ):
			sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
			sents = (sent_detector.tokenize(part, realign_boundaries=True))
			for sentence in sents:
				text = string.replace(text, sentence, "<sentence>"+sentence+"</sentence>")

	#place tags inside sentence
	return re.sub(r'(\.|\?|!)</sentence>', r'</sentence>\1', text)		
	#return text#(re.sub( r'\.\s(.+(?=\.))', r'.<sentence>\1</sentence>', text))

#tags times with start and end times
def output_tagged_time(text):

	#remove first line + PosetedBy to avoid false positives from when email was sent
	text = re.sub(r'PostedBy:.*', "", re.sub(r'^<.*>', "", text))
	
	#get all times, then decide start vs end
	times = []
	for time in re.findall(r'((((0?[0-9]|1[0-9]|2[0-4]):[0-5][0-9](\s?(P|A|p|a)\.?(M|m))?))|((0?[0-9]|1[0-9]|2[0-4])\s?(P|A|p|a)\.?(M|m)))', text):
		times.append(time[0])
	
	timesdict = collapse_times(times)
	finaldict = {}
	#see if there are 2 together, otherwise use select
	jointtimes = re.findall(r'((((0?[0-9]|1[0-9]|2[0-4]):[0-5][0-9](\s?(P|A|p|a)\.?(M|m))?))|((0?[0-9]|1[0-9]|2[0-4])\s?(P|A|p|a)\.?(M|m))| 0?[0-9]| 1(1|2)) ?(-|to) ?((((0?[0-9]|1[0-9]|2[0-4]):[0-5][0-9](\s?(P|A|p|a)\.?(M|m))?))|((0?[0-9]|1[0-9]|2[0-4])\s?(P|A|p|a)\.?(M|m)))', text)
	if (len(jointtimes)>0):
		
	#	print "d"
	#	print timesdict
	#	print "joint"
	#	print jointtimes
		time1 = jointtimes[0][0]
		time2 = jointtimes[0][13]
		print "stime: " + time1
		print "etime: " + time2

		stimes = timesdict[format_time(time1)]
		etimes = timesdict[format_time(time2)]

	else:

		finaldict = select_times(timesdict, text)
		stimes = []
		etimes = []
		if 'stime' in finaldict:
			stimes = timesdict[finaldict['stime']]
		if 'etime' in finaldict:
			etimes = timesdict[finaldict['etime']]

	#return finaldict
	#tag
	final = text

	for s in set(stimes):
		final = string.replace(final, s, "<stime>"+s+"</stime>")
	for e in set(etimes):	
		final = string.replace(final, e, "<etime>"+e+"</etime>")

	return (stimes, etimes)

#when we extract times from the text there can be multiple formats for the same time, 
#to tell the difference between start and end times this needs to be removed, 
#i.e a list ["4.00 PM", "4 pm"] all mean the same actual time
def collapse_times(times):
	#first extract only numerical information
	#reducedtimes = [re.findall(r"(0?[0-9]|1[0-9]|2[0-4])(:|\.)[0-5][0-9]|(0?[0-9]|1[0-9]|2[0-4])", time) for time in times]
	reducedtimes = []
	firstdict = {}
	for time in times:
		shorter = re.findall(r"(((0?[0-9]|1[0-9]|2[0-4])(:|\.)[0-5][0-9])|(0?[0-9]|1[0-9]|2[0-4]))", time)
		if shorter != []:
			#print shorter
			shorttime = shorter[0][0] 
			#print shorttime
			reducedtimes.append(shorttime)

			#put into dict for alter retrieval
			if not shorttime in firstdict:
				firstdict[shorttime] = [time]
			else:
				firstdict[shorttime].append(time)

	twodict = {}
	print reducedtimes
	#convert x to x:00
	formattedtimes = []
	for time in reducedtimes:
		if not(":" in time):
			newtime = time+":00"
		else:
			newtime = time

		formattedtimes.append(newtime)
		
		if newtime in twodict:
			twodict[newtime].extend(firstdict[time])
		else:
			twodict[newtime] = firstdict[time]
	#print "2:"
	#print twodict
	return twodict


	#setify
#	uniquetimes = set(formattedtimes)
	#now we have different times i.e 4 and 4:00 and 4:00 pm will be represented by a single entry 4:00 in the set
	#this can now be used to differentiate strings that represent actual different times
#	return uniquetimes

#makes all time in x:00 format
def format_time(time):
	shorter = re.findall(r"(((0?[0-9]|1[0-9]|2[0-4])(:|\.)[0-5][0-9])|(0?[0-9]|1[0-9]|2[0-4]))", time)
	if shorter != []:
		time = shorter[0][0] 
		if not(":" in time):
			newtime = time+":00"
		else:
			newtime = time
		return newtime

#given a list of talk times decide which are which
def select_times(times, text):
	#print times

	num = len(times)
	if (num==0):
		#nothing
		return {}
	elif (num==1):
	#	print "stime: " + str(times.keys()[0])
		#stime
		return {'stime':times.keys()[0]}
	elif (num==2):
		#at

		#stime and end time
		#get 1st char
		n1 = int(times.keys()[0][0])
		n2 = int(times.keys()[1][0])
		if (n2>n1):
			return {'stime':times.keys()[0], 'etime':times.keys()[1]}
		else:
			return {'stime':times.keys()[1], 'etime':times.keys()[0]}
	else:
		#>2 times
		#what to do?
		return {}	

		# check connected by -???

#get a list of everything enclosed in tags 
def extract_stimes(text):
	times = []
	for possible in (re.findall(r'(?<=<stime>).*(?=<\/stime>)', text)):
		times.append(possible)
	return times

def extract_etimes(text):
	times = []
	for possible in (re.findall(r'(?<=<etime>).*(?=<\/etime>)', text)):
		times.append(possible)
	return times

def extract_paragraphs(text):
	#contents(<paragraph>)(.*\n?)+?.*(?=<\/paragraph>)	
	final = []
	for match in re.findall(r'((<paragraph>)(.*\n?)*?.*(?=<\/paragraph>))', text):
		final.append(remove_tags(match[0]))

	return final

def extract_sentences(text):
	final = []
	for match in re.findall(r'((<sentence>)(.*\n?)*?.*?(?=<\/sentence>))', text):
		final.append(remove_tags(match[0]))
	return final

#extracts already tagged times from files
def get_train_times():
		
	taggedtimes = []

	trainfolder = "files/training/"
	mypath = os.path.dirname(trainfolder)

	print("Train Directory: " + mypath)
	trainfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	for file in trainfiles:
		f = open(mypath+"/"+ file, "r")
		taggedtimes.extend(extract_tagged_times(f.read()))
		f.close()

	return taggedtimes

#adds the <topic> tag line to text
def add_ontology_tag(text):
	topicline = Ontology.get_topic(text)
	return text + "\n\n" + "<topic>"+topicline + "</topic>"

#generic tagger
def find_and_tag(wordstotag, tagname, text):
	#setify, sort by length and tag
	words = list(set(wordstotag))
	words.sort(key=len)

	#initially replace with unique symbol before retagging so no overlap 
	for i in range(len(words)):
		word = words[i]
		text = text.replace(word, "<"+tagname+">|Z|||"+str(i)+"|||Z|</"+tagname+">")

	for i in range(len(words)):
		word = words[i]
		text = text.replace(("|Z|||"+str(i)+"|||Z|"), word)

	return text

