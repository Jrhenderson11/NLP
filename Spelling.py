import sys
import re
import string
from collections import Counter
from collections import Set
	
	
def toLowerWords(string):
	return re.findall(r'\w+', string.lower())

def spellcheck(word):
	
	return

def swap(array, i1, i2):
	a = array[i1]
	b = array[i2]
	newarray = list(array)
	newarray[i1] = b
	newarray[i2] = a 
	return newarray

def edit(word):
	edits = set()
	
	letters=[]
	for letter in word:
		letters.append(letter)
		
	print(letters)
		
	#return set of variations
	
	
	#swap 2 letters
	for iterator in range (len(word)-1, 0, -1):
		
		letter1 = len(word)-1 - iterator
		print("letter1: " + str(letter1))
		
		for i in range(letter1+1, len(word)):
			letter2 = i
			print("swapping " + str(letter1) + " and " + str(letter2))
			newletters = swap(letters, letter1, letter2)
			print(newletters)
			edits.add(''.join(newletters))


	#remove a letter
	for i in range (0, len(word)):
		if (i==0):
			halves = [word[1:len(word)]]
		elif (i==(len(word)-1)):
			halves = [word[0:(len(word)-1)]]
		else: 
			halves = [word[0:i], word[i+1:len(word)]]
		print(halves) 
		#now recombine to get altered word
		if (len(halves)==1):
			edits.add(halves[0])
		else: 
			edits.add(halves[0] + halves[1])
	
	#changing a letter
	for i in range(0, len(word)):
		newletters = list(letters)
		for letter in string.ascii_lowercase:
			if (letter != newletters[i]): 
				newletters[i] = letter
				edits.add(''.join(newletters))
				
				
	#insert new letter
	for i in range(0, (len(word)+1)):
		for letter in string.ascii_lowercase:
			newletters = list(letters)
			newletters.insert(i, letter)
			edits.add(''.join(newletters))

	
	return edits
	
def edit2(orig):
	edits = edit(orig)
	edits2 = set()
	for word in edits:
		edits2 = edits2 | (edit(word))
	
	return edits2
	


def filterKnown(counter, set1):
	known = set(counter)
	return known & set1


def spellcheckFile(fileName):
	#load words counter
	text = (open(fileName).read())
	words = Counter(toLowerWords(text))
	
#	print(words.values())
	
	total = sum(words.values())
	print("sum: " + str(total))
		
	#calculate P(word) as value of word / sum
	
	print("\nEnter word: ")
	word = input()
	print(words[word])
	print('P(' + word + ') =' + str(words[word]/total))
		
	print("edits:")
	edits2 = edit2(word)
	print("filtering")
	candidates = filterKnown(words, edits2)
	print("candidates:")
	print(candidates)

	#sort candidates by stuff

	#make candidates dict with occurences (conjunction between counter and )
	sortedCandidates = {}
	for candidate in candidates:
		sortedCandidates[candidate] = words[candidate]


def finder(fileName):
	file = open(fileName, "r")
	
	phone_book  ={}
	for line in file:
		parts = line.split(":")
		
		if (len(parts) < 2):
			print("invalid phone book file")
			return
		name = parts[0]
		name = name.strip()
		number = parts[1]
		number = number.strip()	
		
		print("\n"+name)
		print(number)
		phone_book[name] = number	


	print("dictionary loaded")
	
	inName = (input("\nEnter a name to query: "))
	inName = inName.strip()
	while ((inName) != "quit"):
		print(phone_book[inName])
		inName = (input("\nEnter a name to query: "))
		inName = inName.strip()
	
	file.close()
