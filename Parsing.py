import nltk 
from nltk import load_parser

grammar1 = nltk.CFG.fromstring("""
	S -> NP VP | Q VP "?"
	VP -> V NP | V NP PP
	PP -> P NP
	V -> "saw" | "ate" | "walked"
	NP -> "John" | "Mary" | "Bob" | Det N | Det N PP | PN
	Det -> "a" | "an" | "the" | "my" 
	N -> "man" | "dog" | "cat" | "telescope" | "park" | "fish" | "fork"
	P -> "in" | "on" | "by" | "with"
	PN -> "She" | "He" | "she" | "he"
	Q -> "Who" | "who"
	""")

#-================================================
			#parsers
parser = load_parser('files/grammar.fcfg', trace=0)

rd_parser = nltk.RecursiveDescentParser(grammar1)

# shift reduce 
sr_parser = nltk.ShiftReduceParser(grammar1)

chart_parser = nltk.ChartParser(grammar1) 

user = ""


#John Smith enjoyed going to the movies. 
#He watches western movies. 
#Jane Lee sometimes went to the cinema with John.
#She didn't like western movies. 
#They watch horror movies.
#Every child likes Kim.
#Kim likes this child. 
#The man used the telescope. 
#The man used the telescope in December. 
#The man used the telescopes with Mary.
#John walked home with Mary.




while user != "quit":
	print("enter string: ")
	user = raw_input()
	for tree in parser.parse(user.split()):
		print(tree)
		#tree.draw() 

