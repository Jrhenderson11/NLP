import re
import os
import nltk
import Code
import pickle
import string
import Tagger
from os import listdir
from nltk.corpus import brown
from nltk.corpus import treebank
from nltk.tag import DefaultTagger
from nltk.tag import UnigramTagger, BigramTagger, TrigramTagger
from os.path import isfile, join, dirname

#stores a list that is used quite a bit
class useful():
	titles = ["Provost", "Professor", "Prof.", "Prof", "Dean", "Associate", "Assistant", "Director", "Dr.", "DR.","Dr", "DR", "Mr.", "MR.", "Mr",  "MR", "Sgt", "Ms.", "Ms", "MS.", "MS", "PhD.", "Ph.D", "PhD", "Candidate"]

#loads words from unix word file
def load_dictionary():
	words = []
	try:
		file = open('/usr/share/dict/words', "r")
			
		for line in file:
			words.append(line.rstrip())	
		file.close()
	except Exception as e:
		print("So you know how the usage info said to run this on a system with a dictionary file?")
		print("you haven't.")
		print("maybe you thought you were being cool")
		print("or maybe you didn't read it")
		print("\n you can press enter to continue and ignore this (name recognition will be worse)" )
		print("Or you can quit and add a dict file")
		print("\n(this is why you should read READMEs)")
		words = ['apple']
		x = raw_input()
	return words

#forgotten what this does, think it was looking for tags of None, either way I can't find where it was used so it can stay for the hell of it
def extract(word):
	return re.match('\b(?:(?!None)\w)+\b', word)

#returns dictionary mapping filename to list of human names in the file
def extract_names_files(filenames):
	
	#load (Trigram) tagger (3% accuracy improvement over unigram)
	file = open("postagger.pickle", "rb")
	tagger = pickle.load(file)
	file.close()
	
	matchregex = re.compile(r'((((D(r|R)\.?|M(r|R)\.?)\s)?[A-Z](\.|\w+)\.?(\s([A-Z](\.|(\w|\-)+)))*)(, Ph\.?D\.?)?)')
	#Load dictionary file
	words = load_dictionary()

	#names is a dictionary between filename and a list of names found in that email
	names = {}
	for filename in filenames:
		text = Code.get_text(filename)

		#filter out PostedBy line (we are only interested in speakers)
		text = re.sub(r'PostedBy:.*', "", re.sub(r'^<.*>', "", text))
	
		#start of sentence = '\.\s([A-Z]\w+(\s([A-Z]\w+))*)'
		#mathces all sequences of 1 or more capitalised words
		startMatches = (re.findall(matchregex, text))
		candidates = []
		#print(startMatches)
		for match in startMatches:
			#print(match)
			tagged = tagger.tag([match[0]])
				
			#tagged[0][0] is word,  tagged[0][1] is tag
			if ((tagged[0][1] in [None]) or (tagged[0][1] in ['NN'])) and (not (tagged[0][0].lower() in words)) and (not ('\n' in tagged[0][0])) and (not is_uppercase_sentence(tagged[0][0], words)):
				candidates.append(tagged[0][0])	
		#print(candidates)
		candidates = filter_acronyms(candidates)
		candidates = filter_part_dates(candidates)
		#print("\n")
		#print(candidates)
		candidates = only_names(candidates)
		#print("\n")
		#print(candidates)
		candidates = remove_places(candidates)
		candidates = filterout_all_titles(candidates)
		#print("\n")
		#print(candidates)
		#put in dictionary
		names[filename] = candidates

	return names

#true = allowed
#Filter function to remove date words from doc (and abbreviations)
def filter_dates(words):
	months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
			, "Monday", "Tuesday", "Wednesday", "Thursday", "Thurs", "Thur", "Friday", "Spring", "Summer", "Fall", "Autumn", "Winter"]
	
	shortmonths = []
	for word in months:	
		shortmonths.append(word[0:3])
		shortmonths.append(word.upper())
	allowed = []	
	for word in words:
		if not( word in months or word in shortmonths or word + "." in shortmonths):
			allowed.append(word)
	return allowed

#filters out strings that contain (not only match) dates
def filter_part_dates(words):
	datewords = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
			, "Monday", "Tuesday", "Wednesday", "Thursday", "Thurs", "Thur", "Friday", "Spring", "Summer", "Fall", "Autumn", "Winter"]
	
	shortdatewords = []
	for date in datewords:	
		shortdatewords.append(date[0:3])

		#also check for allcaps versions
		shortdatewords.append(date.upper())
	datewords.extend(shortdatewords)
	allowed = []	
	for word in words:
		allow = True
		for date in (datewords):
			if not (re.match(("(\s")+date+"|"+date+"\s|^"+date+"$)", word) == None):
				allow = False
				break
		if allow==True: allowed.append(word)
	return allowed

#make words look like names in name files (capitalise first letter)
def name_capitalise(words):
	import string
	capitalised = []
	for word in words:
		capitalised.append(string.capwords(word))
	return capitalised

#filters out all-caps words: Interestingly any 
#tagged name in all caps is always >1 word 
#therefore we can filter out single word acronyms as not names
def filter_acronyms(words):
	allowed = []
	for word in words:
		if (word.split(" ") != [word]) or (word.upper() != word): 
			allowed.append(word)
	return allowed

#Returns only elements of a list that are in the names datasets (custom)
def only_names(words):
	names = {}
	for fname in ["male", "female", "family", "training", "extra"]:
		file = open(("files/names." + fname), "r")
		for name in file.readlines():
			#print(name.rstrip())
			for part in name.split(" "):
				names[part.rstrip()] = True
		file.close()
	namesintext = []

	for word in words:
		total = 0
		titleb = False
		#check if contains title
		for title in useful.titles:
			if title in word:
				namesintext.append(word)
				titleb = True
				break

		#if not title
		if titleb == False:
			parts = word.split(" ")
			for part in name_capitalise(parts):
			#	print("part: " + part)
			#	print((part in names))
				if (part in names):
					total = total + 1
			if total > ((len(parts)/3)):
				namesintext.append(word)
	return namesintext

#filter out names that are places
def remove_places(candidates):
	import Locations
	unwanted = Locations.has_building_words(candidates)
	
	if unwanted != []:
		for item in unwanted:
			candidates.remove(item)
	return candidates

#Used to filter out sentences in uppercase from NER
def is_uppercase_sentence(string, words):
	sentence = string.lower().split(" ")
	count = 0
	if (string.upper() == string) and (len(sentence) > 1):
		for part in sentence:
			if part in words:
				count += 1 
		if (count > (len(sentence)/2)):
			return True
	return False

#Extracts every pretagged name from section of text
def extract_tagged_names(text):
	names = []

	#(<paragraph>)(.*\n?)+?.*(?=<\/paragraph>)
	#old : 
	for possible in re.findall(r'(?<=<speaker>).*(?=<\/speaker>)', text):
		
		#Occasisonally there are 2 speakers next to each other, with unwanted text in the middle e.g
		#Jessie Ramey</speaker> (research opportunities), and <speaker>Judi Mancuso
		#therefore we look for and split this pattern
		final = re.sub('<.*>', '', re.sub('(</speaker>).*(<speaker>)', '|||', possible))
		
		names.extend(final.split("|||"))
	return names

#Extracts every pretagged name from tagged corpus
def get_train_names():
		
	taggednames = []

	trainfolder = "files/training/"
	mypath = os.path.dirname(trainfolder)

	print("Train Directory: " + mypath)
	trainfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	for file in trainfiles:
		f = open(mypath+"/"+ file, "r")
		taggednames.extend(extract_tagged_names(f.read()))
		f.close()

	for name in taggednames:
		if filter_acronyms([name])==[]:
			print(name)

#after a list of names is generated a set of different people is needed (ie Dr Orloff is the same as Professor Ann Orloff)
def collapse_names(names):
	newnames = []
	for name in names:
		#found = False
		newnames.append(name.rstrip())
	
	if '' in newnames:
		newnames.remove('')
	names = newnames
	#now names are just actual names
	#now go and sort names into categories

	#this counts the number of distinct categories (usedto create dict)
	numunique=0
	similarnames = {}
	for name in names:
		if (numunique ==0):
			numunique = numunique +1
			similarnames[0] = [name]
		else:
			found = False
			for i in range(0, numunique):
				nameslist = similarnames[i]
				#look through list and find similarities

				for match in nameslist:
					if (contains_part_name(match, name)):
						#add to current dict
						similarnames[i].append(name)
						found = True
						break
				if (found==True):
					break
			if (found==False):
				#create new category
				similarnames[numunique] = [name]
				numunique = numunique +1
	return similarnames

#returns whether one name shares parts with another
def contains_part_name(s1, s2):
	#first remove titles so that actual names remain 
	#(because Dr Alan is not the same as Dr Bob eventhough both have Dr in)

	for title in useful.titles:
		if title in s2:
			s2 = re.sub(title, "", s2)
		if title in s1:
			s1 = re.sub(title, "", s1)
	#then check same words (+ caps version)
	s2 = re.sub(" ", "", s2)
	for part in s1.split(" "):
		#print(s1.split(" "))
	
		#print((re.match(r'^$', part)))
		part = re.sub(r',', '', part)
		if ((part in s2) or (part.upper() in s2) or (part.lower() in s2) or (name_capitalise([part])[0] in s2)) and (re.match(r'^$', part)==None):
			#print("COMMON: " + part + ":")
			return True
	return False

#filters out names like "Associate Professor" that are entirely titles
def filterout_all_titles(names):
	#print("filter")
	newnames=[]
	for name in names:
		newname = name
		for title in useful.titles:
			newname = re.sub(title, "", newname)
		#	print("new " + newname)
		if (re.match(r'^\s?$', newname) == None):
		#	print("adding '" + newname + "'")
			newnames.append(name)
	return newnames

#This function's job is to remove people who are not speakers
#it does this by eleiminating names that appear at the end of the file (signing off emails) or appear in the PostedBy field
def filter_sender(namesdict, text):
	
	#badlines is a combination of lines with names to blacklist (Postedby and last lines)
	lastline = re.findall(r'.*\n*$', text)
	badlines = ""+lastline[0]
	#badlines = ""
	postedBy = re.findall(r'PostedBy:.*from', text)
	if not (postedBy == None):
		badlines = badlines + " " + postedBy[0]

	#print(badlines)
	filtereddict = {}
	x = 0
	for names in namesdict:
		lastname = False
	#	print(names)
		for name in namesdict[names]:
			if (contains_part_name(name, badlines)):
				#print("FOUND " + name + " IN BLACKLIST")
				#name is sender so dont add
				lastname = True
				break
		#add if is last number
		if (lastname==False):
			filtereddict[x] = namesdict[names]
			x = x + 1

	return filtereddict

#given list of people (in dict format) decide speaker
def pick_speakers(namesdict, text):
	text = Tagger.remove_tags(text)

	speakernums = []
	if "Who:" in text:
		wholine = re.findall(r'Who:.*', text)[0]
		for names in namesdict:
			for name in namesdict[names]:
				if (contains_part_name(name, wholine)):
					speakernums.append(names)
					break
		return speakernums
	max = 0
	index = 0
	for names in namesdict:
		if len(namesdict[names]) > max:
			max = len(namesdict[names])
			index = names

	speakernums = [index]
	index = 0

	#check for indicative words next to speaker
	for names in namesdict:
		for name in namesdict[names]:
			#(("by " + name) in text) or 
			#or (name + ",") in text 
			# or ("  "+name in text)  or ("	"+name in text)
			if (((name + " will") in text)):
				speakernums.append(names)
				break
	return speakernums
