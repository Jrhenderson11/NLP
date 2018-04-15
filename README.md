# NLP

## Overview: 

This repo is for natural language processing stuff, most of the stuff here is from a university module coursework which was a massive and interesting project. The task was, given a corpus of emails about lectures, to pick out some key information from each like where / when it was and the name of the speaker, and to attempt to categorise the email into the relevant subject. The final report submitted for this work is in NLPReport.pdf, it is a little squished and badly presented since we were given a page limit and I really wanted to put as much detail in as possible, in the end I got 100% on the assingment.

Since I enjoyed the module and I think the coursework is really interesting I'm going to try and extend it and add some new features such as the ones I suggested in the report.

-----------------
**Everything past here is the original readme stuff, but it's messy and disorganised so I'll try to slowly rewrite it**
		
## Usage:

Please run in the folder from the zip, the program assumes the files are where it expects them to be

To run the program in the way intended for the assignment type into a terminal 

				'python Code.py <files>'

where **\<files\>** is a sequence of 0 or more filenames or any other indicator of a list of files (e.g ./files/test_untagged/* will give every file in the folder file as a parameter)


	***TO USE THE SYSTEM IN THE WAY INTENDED RUN WITH PYTHON 2.7 AND ./files/test_untagged/* THIS IS HOW IT KNOWS WHERE THE DATA IS***

The system expects to find 3 folders in its file directory: test_untagged, test_tagged and my_tagged, the first 2 are the corpus and the last is where it saves its own tagged files

To view this usage information run 'python Code.py -h'

If you wish to inspect each email individually you can set the variable stopping (line 163 Code.py) to True and the system will pause and ask for user input after processing each email. This allows you to take a look at the output of the system for each tag type.

----------------------------------

## Files (relevant to the assignment):

CODE:

 - Code.py: Main functionality (called code because was originally used as text en/decoding)

 - Tagger.py: Responsible for tagging untagged files

 - NER.py: Has methods for NER extraction

 - Classifier.py: contained training and classification methods using naive bayes for 2nd part of Assignment (depreciated)

 - Intro.py: fun little bit to help the intro art

 - Locations.py: a location tagger

 -Onotology.py: tags topics and sorts into an ontology tree

- Eval.py: calculates accuracy, precision, recall and f measure for each tag

OTHER:

 - README.md: This document

 - postagger.pickle: stores the POS tagger that is built spearately		

 - FILES/: contains files used for training such as names datasets and the emails and lists of already tagged speakers / locations, is parent folder for training and test data folders

## Files (stuff not crucial to the coursework):

 - Classifier.py: naive bayes classification stuff

 - Clusterer.py: currently just a scratch pad for some ideas about representing the ontology using clustering algorithms

 - Foxer.py: a script to help solve a riddle / puzzle thing using NLP techniques, basically finds an intersection between subjects e.g. tintin character and govenor of india

 - generate_phone_book.py: generates a random phonebook as training / test data for something

 - indian.py: a proceesing script for turning a csv of indian names into a list

 - ldademo.py: stub of a script to use LDA as a topic selection algorithm

 - lemmandstem.py: a script with lemming and stemming stuff

 - NLP1.py: code for part 1 of the assignment (duplicate of code from Code.py)

 - Parsing.py: a script demonstrating parsing using context-free-grammars

 - Spelling.py: experimenting with spelling corrction / error detection

 - subjecter.py: a short preprocessing script to turn a list scraped off a website of subject words into a usable list (used to make files/sublist.txt) 

 - taggertest.py: building and testing different POS taggers (the measurements here aren't representative of the utility of using a POS tagger in the assignment, relying on POS tags can be restrictive and the more accurate the tags the more restrictive sometimes)

 - tf-idf.py: file containing multiple agorithms that would use a TF-IDF matrix generated from the email data (very WIP)

 - trainer.py: brief thing based on part of taggertest.py used to train and save a single tagger (used to make POS.pickle for the assignment)

 - vectorize.py: creating a TF-IDF matrix from a corpus using gensim (taken from gensim website)

 - wikifier.py: some basic code for analysing wikipedia articles for useful info (theoretically could be used to assist with NER but I found performance was poor)

 - word2vec.py: playing around for using word2vec and testing similarity (used to help calibrate Ontology topicWord selection)

--------------------------------
## Basic Overview:

This system comprises of multiple python files. It is written in python 2.7 and should be run using a suitable interpreter.

the system it is run on will need nltk with several downloaded modules:
brown, ieer, semcor, penn treebank and wordnet from corpora
punkt and the universal tagset from models
as well as gensim

Code.py is the main file, it is responsible for the file handling and calling the methods from other files to do the fiddly bits. What these fiddly bits should be self explanatory from their names, if not look at the above section on Files

## Phases:

Running Code.py demonstrates both parts of the assignment and prints information to the console. It reads in the untagged files, extracts information (and displays a summary to the console for inspection), saves the tagged files, all the time comparing its performance to the test data, displaying summary statistics at the end. It then creates the ontology tree and prints it to console

### Fun Fact #1: 
Intro.py selects its 3 random words from Big.txt, because Big.txt contains the text from Tolstoys "War and Peace"
it therefore has a preference for words from this book; especially Pierre, Paris and Napoleon.


## Custom input data:

I've modified the contents of the names files from nltk to remove words that commonly provide false positives 
ie the word "Urban" in names.family

I've also added a file containing names found by extracting pretagged speakers (names.training) and names.extra, which contains titles and abbreviated middle name letters (e.g Thomas W. Malone)

These improvements are an important factor in the systems performance in the NER stage

### Fun Fact #2:
 The system uses 74 regular expressions!
