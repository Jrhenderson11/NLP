import re
import NER
import Code
import pprint
import gensim
import Tagger
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize

#removes part of type line that is not relevant for topic
def take_out(word, text):
	if "cmu.andrew.org." in classification:
		classification = re.sub(r'cmu\.andrew\.org\.', "", classification)
	return text

#looks for indicators of the topic (extracts lists of keywords)
def get_topic(origtext):

	text = Tagger.remove_tags(origtext)
	topic = ""
	
	typer = re.findall("Type:\s(.*)", text)[0]
	typeline = re.findall("\s.*", typer)[0].lstrip()
	for word in ["cmu.andrew.org.", "cmu.andrew.", "heinz"]:
		typeline = typeline.replace(word, "")
	
	typeline = re.sub(r'\.', " ", typeline)
	topic = topic + typeline.strip() + " " + typeline.strip()+ " "#

	#add to weighting of cs to prevent the letters cs being overlooked
	if ".cs" in typeline:
		topic = topic + " computer science"
	
	quotes = re.findall(r'("(.*\n?.*)")', text)

	finquotes = set()
	
	for quote in quotes:
		finquotes.add(quote[0].replace("\"", ""))
	
	if not ("case study" in text):
		#print("quotes: ")
		for quote in finquotes:
			#print(quote	)
			topic = topic + quote + " "
	
	#get topic line
	if "Topic:" in text: 
		topicline = re.findall("Topic:\s(.*)", text)[0]
		topic = topic + (re.findall("\s.*", topicline)[0].lstrip())

		badwords = [ "fwd", "seminar", "lecture", "presentation", "talk", "reminder", "cmu"]
		#filter stopwords
		stopfile = open("files/stopwords.txt", "r")
		stopwords = stopfile.readlines()
		stopfile.close
		topic = topic.replace(":", "")
		#print(badwords)

		for word in badwords:
			topic = topic.replace(word, "")
			topic = topic.replace(word.upper(), "")
			topic = topic.replace(NER.name_capitalise([word])[0], "")		
		
		
		topic = re.sub(r'[0-9]*', "", topic)
		topic = re.sub(r',', " ", topic)
		#make all single spaces
		topic = re.sub(r'\s+', " ", topic)
		topicwords = re.split(r'\s', topic)
		
		for wordx in stopwords:
			word = wordx.strip()
			if word in topicwords:
				topicwords.remove(word)
			if (word.upper()) in topicwords:
				topicwords.remove(word.upper())
			capital = (NER.name_capitalise([word])[0]) 
			if capital in topicwords:
				topicwords.remove(capital)

	#look for subject words
	subfile = open("files/sublist.txt", "r")
	subjectwords = subfile.readlines()
	subfile.close()

	#tokenise so we can match with whole words
	textwords = word_tokenize(text)

	#as whole words
	for wordx in subjectwords:
		word = wordx.strip()
		if word in textwords or (word.upper()) in textwords or (NER.name_capitalise([word])[0]) in textwords:
			topicwords.append(word)


	#filter out dates		
	topicwords = NER.filter_dates(topicwords)

	#remove unwanted punctuation

	if "&" in topicwords:
		topicwords.remove("&")
	if "/" in topicwords:
		topicwords.remove("/")
	final = set()
	#lower
	for word in topicwords:
		final.add(word.lower())

	return (" ".join(final)).strip()

class Ontology():

	def __init__(self):
		self.ontology = ontology = { 'Top' :
											 { 'arts' : 
											 			{ 'art' : 
											 						{ 'topicWords' : [ 'art', 'artist', 'painting'], 'talks' : list()}
											 			, 'other'   : 
											 						{'topicWords' : [ 'arts', 'philosophy', 'english', 'language'], 'talks' : list()}					 			
														}
											 , 'humanities' : 
														{ 'politics' : 
											 						{ 'topicWords' : [ 'politics', 'politician', 'law'], 'talks' : list()}
											 			, 'sociology' : 
											 						{ 'topicWords' : [ 'sociology', 'social', 'customs', 'behaviour', 'communities'], 'talks' : list()}					 			
											 			, 'history' : 
											 						{ 'topicWords' : [ 'history', 'civilisation', 'ancient'], 'talks' : list()}
														}
											 , 'science' : 
														 { 'physics' : 
											 						{ 'particle-physics' : 
											 									{ 'topicWords' : [ 'physics', 'particle', 'proton', 'atomic'], 'talks' : list()}
														 			, 'astro-physics' : 
														 						{ 'topicWords' : [ 'physics', 'astrophysics', 'astronomy', 'star', 'stars'], 'talks' : list()}					 			
														 			, 'general-physics' : 
														 						{ 'topicWords' : [ 'physics', 'science', 'forces'], 'talks' : list()}
																	}
											 			, 'biological' : 
											 						{ 'medicine' : 
											 									{ 'topicWords' : [ 'medicine', 'medical', 'health', 'pharmaceutical', 'patient'], 'talks' : list()}
														 			, 'biology' : 
														 						{ 'topicWords' : [ 'biology', 'cell', 'science'], 'talks' : list()}
																	}
											 			, 'chemistry' : 
											 						{ 'topicWords' : [ 'chemistry', 'chemical', 'interaction'], 'talks' : list()}
											 			, 'CS' : 
											 						{ 'hci' : 
											 									{ 'topicWords' : [ 'cs', 'computer', 'science', 'hci', 'HCI','human', 'interaction', 'user'], 'talks' : list()}
														 			, 'vision' : 
														 						{ 'topicWords' : [ 'cs', 'computer', 'science','vision', 'AI', 'edge', 'detect'], 'talks' : list()}					 			
														 			, 'robotics' : 
														 						{ 'topicWords' : [ 'cs', 'computer', 'science','robotics', 'robot', 'intelligence', 'autonomous'], 'talks' : list()}
														 			, 'nlp' : 
														 						{ 'topicWords' : [ 'cs', 'computer', 'science','linguistics', 'language', 'semantics', 'syntax'], 'talks' : list()}
														 			, 'software-eng' : 
														 						{ 'topicWords' : [ 'cs', 'computer', 'science','programming', 'system', 'design'], 'talks' : list()}
														 			, 'general-compsci' : 
														 						{ 'topicWords' : [ 'cs', 'computer', 'science', 'AI', 'machine', 'learning', 'program', 'system', 'security', 'network'], 'talks' : list()}
																	}
											 			, 'materials' : 
											 						{ 'topicWords' : [ 'materials', 'metals', 'polymer'], 'talks' : list()}
											 			, 'engineering' : 
											 						{ 'topicWords' : [ 'engineering', 'design', 'build'], 'talks' : list()}

														}
											 
											 , 'other' : 
											 			{ 'teaching' : 
											 						{ 'topicWords' : [ 'teaching', 'education', 'mam'], 'talks' : list()}
											 			, 'economics' : 
											 						{ 'topicWords' : [ 'economics', 'monetary', 'policy', 'model', 'fiscal'], 'talks' : list()}					 			
											 			, 'law' : 
											 						{ 'topicWords' : [ 'law', 'legal', 'court'], 'talks' : list()}
														}
											}
									}
		self.traversal_info = self.generate_traverse_dict(self.ontology, {}, "")
		print(self.traversal_info)
	
	def get_topicwords(self, location, path):
		keys = location.keys()
		if  'topicWords' in keys: 
			return location['topicWords']
		nextpart = path.split(",")[0]
		if not nextpart in keys:
			print("bad path: " + nextpart)
			return
		return self.get_topicwords(location[nextpart], ",".join(path.split(",")[1:]))

	#create traversal dictionary to quickly find locs in tree
	def generate_traverse_dict(self, location, locationdict, path ,key=None):
		
		keys = location.keys()

		#only map leaf nodes
		if  'topicWords' in keys: 
			locationdict[key] = path[1:]#location
			return locationdict 
		else:
			for key in keys : 
				locationdict = self.generate_traverse_dict(location[key], locationdict, path + "," + key,key)
			return locationdict

	def add_topics_interactive(self, topic, fileName):# or do this manually.
		print('Topic: ' + topic) 
		#print(self.print())  ## define this.
		input_class   = input('Enter Class:')
		input_words = input('Class words:')
		if input_class not in input_words:
			input_words = input_words + ", " + input_class
		self.traverse[input_class.rstrip()]['topicWords'] += input_words.rsrip().split( ',' )

	def insert_batch(self, files):
		print("loading word2vec model")
		model = gensim.models.KeyedVectors.load_word2vec_format('files/GoogleNews-vectors-negative300.bin', binary=True)
		pp = pprint.PrettyPrinter(indent=4)
		for file in files:
			print("inserting " + file )
			self.insert_topic(file, model)
		pp.pprint(self.ontology)
			#raw_input()

	def insert_topic(self, fileName, model):
		# use word2vec to find similarity between words in topic
		#and 'topic_words'. Closest is correct 

		#topicline:
		topic = re.findall(r'((?<=<topic>).*(?=<\/topic>))', Code.get_text(fileName))[0].strip()

		scores = {}
		for leaf in self.traversal_info.keys():
		#	print("leaf")
		#	print(leaf)
			topicWords = self.get_topicwords(self.ontology, self.traversal_info[leaf])
			scores[self.calc_similarity(topic.split(" "), topicWords, model)] = leaf  
			#find distance using word2vec and some other stuff? 
		maximum = max(scores.keys())
		c = scores[maximum]
		print("best class is:")
		print(c )

		loc = self.traversal_info[c]
		print("loc:")
		print(loc)
		self.ontology = self.add_to_topic(fileName, loc, self.ontology)
		#self.ontology[loc]['list'].append(fileName)
	
	def add_to_topic(self, fileName, path, location=None):
		keys = location.keys()
		if  'talks' in keys: 
			#insert into leaf
			#print(location.keys())
			if location['talks'] == None:
				print("inserted " + fileName + " into None" )
				location['talks'] = []
			#print(location['talks'].append(fileName))

			#location['talks'] = 
			location['talks'].append(fileName)
			return location
		else:
			nextpart = path.split(",")[0]
			if not nextpart in keys:
				print("bad path: " + nextpart)
				return
			#self.add_to_topic(fileName, ",".join(path.split(",")[1:]), location[nextpart])
			location[nextpart] = self.add_to_topic(fileName, ",".join(path.split(",")[1:]), location[nextpart])
			return location

	#given 2 lists of words meaures the simialrity
	def calc_similarity(self, candidatewords, topicwords, model):
		total = 0
	
		subjectwords = []
		subfile = open("files/sublist.txt", "r")
		for line in subfile.readlines():
			subjectwords.append(line.strip())
		subfile.close()
		valtop = 0
		valtagged = 0
		for word in candidatewords:
			if word in model.wv.vocab:
				valtagged = valtagged + 1

		for poss in topicwords:
			if poss in model.wv.vocab:
				valtop = valtop + 1


		for word in candidatewords:
			for poss in topicwords:
				distance = 0

				if word in subjectwords: 
					if poss == word:
						distance = 2
					else:
						if (poss in model.wv.vocab) and (word in model.wv.vocab):
							distance= 2 * model.similarity(poss, word)
				else:
					if poss == word:
						distance = 1
					else:
						if (poss in model.wv.vocab) and (word in model.wv.vocab):
							distance = model.similarity(poss, word)
				total = total + distance
		#return (total / (valtop + valtagged))
		return (total / (len(candidatewords) + len(topicwords)))

	def remove_topicwords(self, location):
		keys = location.keys()
		if  'topicWords' in keys: 
			#insert into leaf
			#print(location.keys())
			if location['talks'] == None:
				print("inserted " + fileName + " into None" )
				location['talks'] = []
			#print(location['talks'].append(fileName))

			#location['talks'] = 
			location['talks'].append(fileName)
			return location
		else:
			nextpart = path.split(",")[0]
			if not nextpart in keys:
				print("bad path: " + nextpart)
				return
			#self.add_to_topic(fileName, ",".join(path.split(",")[1:]), location[nextpart])
			location[nextpart] = self.add_to_topic(fileName, ",".join(path.split(",")[1:]), location[nextpart])
			return location

