import re
import os
import NER
import Tagger
from os import listdir
from os.path import isfile, join, dirname

#def get_locations(text):
	#out of 329 locations from tagged data 8 are just numbers, and in fact only 2 unique (8220 and 2110), these can be found in files, no poin in matching regex with this
#((([A-Z]\w+)|[0-9]+)(,? (([A-Z]\w+|[0-9]+)))*)

#total: ((([A-Z]\w+)|1st|2nd|3rd|4th|[0-9]+)(,? (([A-Z]\w+|1st|2nd|3rd|4th|[0-9]+)))*)

#few false positives (FILTER OUT DATES!!!!!!!!) ([A-Z]\w+ )+[0-9]\w+ and very few partials!

#better: ((([A-Z]\w+)|1st|2nd|3rd|4th|[0-9]+[A-Z]*)((,? ((room|in) )?)(([A-Z]\w+|1st|2nd|3rd|4th|[0-9]+[A-Z]*)))+)
#does not segment with lowercase in / room
#for those that are missed out we have: ( (([A-Z]+[0-9]+)|([0-9]+[A-Z]+)) ) spaces avoid in middle of other rooms

#few are single words
#those that are are mostly ABC123 format so can matched with a single regex

#((([A-Z]\w+)|1st|2nd|3rd|4th|5th|6th|[0-9]+[A-Z]*)((,? ((room|in) )?)(([A-Z]\w+|1st|2nd|3rd|4th|5th|6th|[0-9]+[A-Z]*)))+)

#try the reverse: ([0-9]\w+ )([A-Z]\w+)+ doesnt quite work (mainly picks out parts of larger locs)

#returns a list of anything in location tags
def extract_tagged_locations(text):
	locations = []
	matches2 = re.findall(r'((?<=<location>)(.*\n)*?.*(?=<\/location>))', text)
 
	for possible in matches2:
		#print(possible)
		s = ''
		try:
			s = re.sub(r'(</location>).*(\n.*)*(<location>)', '|||', possible)
		except:
			s = re.sub(r'(</location>).*(<location>)', '|||', possible[0])
		final = re.sub('<.*>', '', s)
		locations.extend(final.split("|||"))

	#print(locations)
	return locations

#this extracts everything from the emails "Place:" header if it exists
def place_field(text):
	import Tagger
	if "Place:" in text:
		placeline = re.findall(r"(?<=\nPlace:)\s((.*\n)+?)(?=>?\w+:)", text)
		if not placeline == []:
			place = Tagger.remove_tags(placeline[0][0])
			return [place]
	return []
		
#looks for simple Word number combinations 
#these provide few false positives once dates are removed
def filter_basic(candidates):
	import NER
	matches = []
	for word in candidates:
		if re.match("([A-Z]\w+ )+[0-9]\w+", word):
			matches.append(word)

	return NER.filter_part_dates(matches)

#try and find numbers on a newline cut off from other locations
def experimental_newline_number(text):
	for match in re.findall(r'(?<=\n)[0-9]+', text):
		print(match[0] )

#filter to see if match looks like location
def has_building_words(candiates):
	import NER
	#so happy someone spells centre correctly! now I can add it to my list of building words and its useful (email 284 btw)
	building_words = ["room", "building", "hall", "auditorium", "wing", "floor", "center", "centre", "school", "theater", "theatre", "library", "university", "tower", "college", "institute", "avenue"]
	#add capitalised versions as well
	building_words.extend(NER.name_capitalise(building_words))
	contain = []
	for line in candiates:
		for word in building_words:
			if word in line:
				contain.append(line)
				break
	return contain

#Extracts every pretagged name from tagged corpus
def get_train_locations_files():
	taggedlocations = []

	trainfolder = "files/training/"
	mypath = os.path.dirname(trainfolder)

	print("Train Directory: " + mypath)
	trainfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	for file in trainfiles:
		f = open(mypath+"/"+ file, "r")
		taggedlocations.extend(extract_tagged_locations(f.read()))
		f.close()
	print("PLACES:")
	for place in taggedlocations:
		print(place)

#checks to see if location has appeared in previous tagged emails
def is_known(word):
	known = set()
	file = open("files/places.txt")
	for line in file.readlines():
		known.add(line.rstrip())
	file.close()
	return (word in known)

#main function for getting a list of all locations in an untagged document
def get_all_locations(text):
	firstcandidates = []
	candidates = []
	final = []
	basics = []
	
	firstlist = re.findall(r'(((([A-Z]\w+)|1st|2nd|3rd|4th|5th|6th|(r|R)o(o|m)m|[0-9]+[A-Z]*)((,? (((r|R)o(o|m)m|in) )?)(([A-Z]\w+|1st|2nd|3rd|4th|5th|6th|hall|Hall|[0-9]+[A-Z]*)))+)(\n\s?((([A-Z]\w+)|1st|2nd|3rd|4th|5th|6th|(r|R)o(o|m)m|[0-9]+[A-Z]*)((,? (((r|R)o(o|m)m|in) )?)(([A-Z]\w+|1st|2nd|3rd|4th|5th|6th|hall|Hall|[0-9]+[A-Z]*)))*))*)', text, re.MULTILINE)
	
	bas = (re.findall("(([A-Z]\w+ )+[0-9]\w+)", text))
	if not bas == []:
		for match in bas:
			basics.append(match[0].strip())

	final.extend(NER.filter_part_dates(basics))

	
	for match in firstlist:
		#print(match[0])
		#raw_input()
		firstcandidates.append(match[0].strip())
	
	#strip one word line off
	for candidate in firstcandidates:
		#print(candidate)
		#print(re.findall(r'\n\s?\w+(\s|\n)?$', candidate))
		#raw_input()
		if (re.findall(r'\n\s?\w+(\s|\n)?$', candidate) == ['']):
			candidates.append(re.sub(r'\n\s?\w+(\s|\n)?', "", candidate))
		else:
			candidates.append(candidate)

	for match in has_building_words(candidates):
		final.append(match.strip())
	for match in filter_basic(candidates):
		final.append(match.strip())

	#final.extend(place_field(text))

	return set(final)

#given a list of possible locations picks the most likely
def pick_locations(candidates, text):
	text = Tagger.remove_tags(text)
	#if 1 just go for it
	if len(candidates) ==1:
		return candidates
	best = []
	goodlocwords = ["room", "Room", "hall", "Hall"]
	#look for room / hall
	i = False
	
	#for candidate in candidates:
	#	if (("in " + candidate) in text) or (candidate in place_field(text)):
			#best.append(candidate)
	#		i=True
	#if i:
	#	return best

	for candidate in candidates:
		for word in goodlocwords:
			if word in candidate:
				best.append(candidate)
				break
	best.extend(filter_basic(candidates))

	return best