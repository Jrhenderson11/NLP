from random import randint
import nltk
import nltk.data

#makes pretty pictures
def print_intro():
	print ("==========================")
	print ("|		         |")
	print ("|	     | 		 |")
	print ("|	 |\  | |\	 |")
	print ("|	       |  	 |")
	print ("|________________________|")
	print ("==========================")
	#26

	words = print_words()
	l = len(words)
	while l >26:
		words = print_words()
		l = len(words)
	print((" " * ((26-l)/2))+words)
	print ("_________________________")


#does fun stuff, not very efficient 
def print_words():
	n = []
	l = []
	p = []
	for line in (nltk.data.load('files/big.txt').split(" ")):
		for char in ['\n', ',', '.']:
			if char in line: line = line[:line.index(char)]
		if len(line)>0:
			c = line[0].lower()
			if (c=='n'): n.append(line) 
			elif (c=='l'): l.append(line)
			elif (c=='p'): p.append(line)
	return ((n[randint(0, len(n)-1)])+' '+(l[randint(0, len(l)-1)])+' '+(p[randint(0, len(p)-1)])).title()