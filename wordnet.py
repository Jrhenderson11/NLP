import re
import nltk
#from nltk.corpus import ieer
from nltk.corpus import wordnet as net,ieer, semcor

def gethypernymtree(meaning):
	list = meaning.hypernyms()
	newlist = []
	for mean in list:
		newlist.append(gethypernymtree(mean))
	return (list + newlist)

print "user input(1) or semcor(2)?"

num = raw_input()

if num == "1":
	#input
	print "enter word"
	word = raw_input()
	for meaning in (net.synsets(word)):
		#print "Sense: " + re.findall("'.*'", str(meaning))[0]
		print "Sense: " + str(meaning)
		print meaning.definition() + "\n"	
		hypernyms = (meaning.hypernyms())
		if len(hypernyms) > 0:
			print "\nHypernyms:"
			for meaning2 in hypernyms:
				print re.findall("'.*'", str(meaning2))[0]
		
		hyponyms = (meaning.hyponyms())
		if len(hyponyms) > 0:
			print "\nHyponyms:"
			for meaning2 in hyponyms:
				print re.findall("'.*'", str(meaning2))[0]
			
#		print "\nHypernym Tree:"
#		print (gethypernymtree(meaning))
		print "\n"

#		dog = wn.synset('dog.n.01')
#		hypo = lambda s: s.hyponyms()
#	 	hyper = lambda s: s.hypernyms()
		#list(dog.closure(s.hypernyms(), depth=1)) == dog.hypernyms()
#True
#>>> list(dog.closure(hyper, depth=1)) == dog.hypernyms()

elif (num=="2"):
	#semcor
	print "semcor"

	for line in	semcor.sents()[0:100]:
		s = ""
		for word in line:
			s = s + " " + word 
		print s + "\n"

		for word in line:
			meanings = net.synsets(word)
			if len(meanings) > 0: 
				print meanings[0].definition()
elif num == "3":

	docs = ieer.parsed_docs('APW_19980424')
	tree = docs[1].text
	
	from nltk.sem import relextract
	pairs = relextract.tree2semi_rel(tree)
	for s, tree in pairs[18:22]:
		print('("...%s", %s)' % (" ".join(s[-5:]),tree))

	reldicts = relextract.semi_rel2reldict(pairs)
	for k, v in sorted(reldicts[0].items()):
	 	print(k, '=>', v)

#	The function relextract() allows us to filter the reldicts 
#	according to the classes of the subject and object named entities. 
#	In addition, we can specify that the filler text has to match a given regular expression,
#	 as illustrated in the next example. Here, we are looking for pairs of entities in the IN 
#	relation, where IN has signature <ORG, LOC>.
	IN = re.compile(r'(\s?[a-z].*)?\bin\b(?!\b.+ing\b)')
	for fileid in ieer.fileids():
		print fileid
		for doc in ieer.parsed_docs(fileid):
			for rel in relextract.extract_rels('ORG', 'LOC', doc, corpus='ieer', pattern = IN):
				print(relextract.rtuple(rel)) # doctest: +ELLIPSIS


	roles = "(.*(analyst|commissioner|professor|researcher|(spokes|chair)(wo)?m(e|a)n|writer|secretary|manager|commander|boss|founder)\s(of|in|for) (the)?)"
			
	ROLES = re.compile(roles, re.VERBOSE)
	for fileid in ieer.fileids():
	   for doc in ieer.parsed_docs(fileid):
	      for rel in relextract.extract_rels('PER', 'ORG', doc, corpus='ieer', pattern=ROLES):
	          print(relextract.rtuple(rel)) # doctest: +ELLIPSIS