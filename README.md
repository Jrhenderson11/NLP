Overview of NLP System
		
Usage:
Please run in the folder from the zip, the program assumes the files are where it expects them to be

To run the program in the way intended for the assignment type into a terminal 

				'python Code.py <files>'

where <files> is a sequence of 0 or more filenames or any other indcator of a list of files (e.g ./files/test_untagged/* will give every file in the folder file as a parameter)


	***TO USE THE SYSTEM IN THE WAY INTENDED RUN WITH PYTHON 2.7 AND ./files/test_untagged/* THIS IS HOW IT KNOWS WHERE THE DATA IS***

The system expects to find 3 folders in its file directory: test_untagged, test_tagged and my_tagged, the first 2 are the corpus and the last is where it saves its own tagged files

To view this usage information run 'python Code.py -h'

If you wish to inspect each email individually you can set the variable stopping (line 163 Code.py) to True and the system will pause and ask for user input after processing each email. This allows you to take a look at the output of the system for each tag type.

================================
Files:

	CODE:

		-Code.py: Main functionality (called code because was originally used as text en/decoding)
 
		-Tagger.py: Responsible for tagging untagged files

		-NER.py: Has methods for NER extraction

		-Classifier.py: contained training and classification methods using naive bayes for 2nd part of Assignment (depreciated)

		-Intro.py: fun little bit to help the intro art

		-Locations.py: a location tagger

		-Onotology.py: tags topics and sorts into an ontology tree

		-Eval.py: calculates accuracy, precision, recall and f measure for each tag

	OTHER:

		-README.md: This document

		-postagger.pickle: stores the POS tagger that is built spearately		

	FILES/: contains files used for training such as names datasets and the emails and lists of already tagged speakers / locations, is parent folder for training and test data folders

================================

Basic Overview:

This system comprises of multiple python files. It is written in python 2.7 and should be run using a suitable interpreter.

the system it is run on will need nltk with several downloaded modules:
	brown, ieer, semcor, penn treebank and wordnet form corpora
	punkt and the universal tagset from models

Code.py is the main file, it is responsible for the file handling and calling the methods from other files to do the fiddly bits. What these fiddly bits should be self explanatory from their names

Phases:

	running Code.py demonstrates both parts of the assignment and prints information to the console. It reads in the untagged files, extracts information (and displays a summary to the console for inspection), saves the tagged files, all the time comparing its performance to the test data, displaying summary statistics at the end. It then creates the ontolgy tree and prints it to console


Fun Fact #1: Intro.py selects its 3 random words from Big.txt, because Big.txt contains the text from Tolstoys "War and Peace"
It therefore has a preference for words from this book; especially Pierre, Paris and Napoleon.


FILES

I've modified the contents of the names files from nltk to remove words that commonly provide false positives 
ie the word "Urban" in names.family

I've also added a file containing names found by extracting pretagged speakers (names.training) and names.extra, which contains titles and abbreviated middle name letters (e.g Thomas W. Malone)


FUN FACT #2: The system uses 74 regular expressions
