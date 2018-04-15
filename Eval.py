import NER
import sys
import Code
import Locations
#prints help text
def print_help():
	print("\n				HELP TEXT")
	print("\n	To run the program type into a terminal: 'python Eval.py <files>'")
	print("	where <files> is a sequence of 0 or more filenames")
	print("	or any other indcator of a list of files (e.g ./files/*)")
	print("\nThis will then evaluate the tagging compared to the tags found in files/test_tagged/")

def print_intro():
	print(("=========================="))
	print(("|                        |"))
	print(("| ____  _  _  __    __   |")  )
	print(("|( ___)( \/ )/__\  (  )  |"))
	print(("| )__)  \  //(__)\  )(__ |"))
	print(("|(____)  \/(__)(__)(____)|"))
	print(("|________________________|  er"))
	print(("\/\/\/\/\/\/\/\/\/\/\/\/\/\n"))

#fileName of evaluated tex, words that have been tagged, acwords that should be tagged
def evaluate_generic(fileName, words, acwords):	
	#text = Code.get_text(fileName)
	fp = 0.0
	fn = 0.0
	tn = 0.0
	tp = 0.0
	
	for word in acwords:
		if word in words:
			tp = tp + 1
		else:
			fn = fn + 1
	for word in words:
		#print(word)
		#ADJUSTED
		if not word in acwords:
			fp = fp + 1

	acc=0
	if (tp + tn + fp + fn) >0:
		acc = (tp + tn) / (tp + tn + fp + fn)
	#if both are empty we have 100% accuracy
	if acwords == words and acwords == []:
		acc = 1
	
	precision = 0
	if len(words) > 0:
		precision = tp / (tp + fp)

	recall = 0
	if len(acwords) >0:
		recall = tp / len(acwords)

	if (precision + recall == 0):
		f1 = 0
	else:
		f1 = 2*((precision * recall) /(precision + recall))
	
	print("Time evaluation of file " + fileName)
	print("accuracy: " + str(acc))
	print("precision: " + str(precision))
	print("recall: " + str(recall))
	print("f1: " + str(f1) )
	#raw_input()
	return (acc, precision, recall, f1)

#gives evaluation for people
def evaluate_speakers(fileName, speakers, notspeakers, acnames):

	text = Code.get_text(fileName)
	#acnames = NER.extract_tagged_names(text)

	fp = 0.0
	fn = 0.0
	tn = 0.0
	tp = 0.0
	
	for name in acnames:
		if name in speakers:
			tp = tp + 1
		else:
			fn = fn + 1
	for name in speakers:
		#print(name)
		#ADJUSTED
		if not name in acnames:
			found = False
			for acname in acnames:
				if NER.contains_part_name(name, acname):
					found =True
					break
			if not found:
				fp = fp + 1

	for name in notspeakers:
		if not name in acnames:
			tn = tn + 1

	acc=0
	if (tp + tn + fp + fn) >0:
		acc = (tp + tn) / (tp + tn + fp + fn)
	#if both are empty we have 100% accuracy
	if acnames == speakers and acnames == []:
		acc = 1
	
	precision = 0
	if len(speakers) > 0:
		precision = tp / len(speakers)

	recall = 0
	if len(acnames) >0:
		recall = tp / len(acnames)

	if (precision + recall == 0):
		f1 = 0
	else:
		f1 = 2*(precision * recall  /(precision + recall))
	
	print("evaluation of file " + fileName)
	print("accuracy: " + str(acc))
	print("precision: " + str(precision))
	print("recall: " + str(recall))
	print("f1: " + str(f1) )
	return (acc, precision, recall, f1)

#gives evaluation for locations
def evaluate_locations(fileName, locs, notlocs, aclocs):
	text = Code.get_text(fileName)

	fp = 0.0
	fn = 0.0
	tn = 0.0
	tp = 0.0
	
	for location in aclocs:
		if location in locs:
			tp = tp + 1
		else:
			fn = fn + 1
	
	for location in locs:
		if not location in aclocs:
			fp = fp + 1

	for location in notlocs:
		if not location in aclocs:
			tn = tn + 1
	
	acc=0
	if (tp + tn + fp + fn) >0:
		acc = (tp + tn) / (tp + tn + fp + fn)
	
	if aclocs == locs and aclocs == []:
		acc = 1
	
	precision = 0
	if len(locs) > 0:
		precision = tp / len(aclocs)

	recall = 0
	if len(aclocs) >0:
		recall = tp / len(aclocs)

	if (precision + recall == 0):
		f1 = 0
	else:
		f1 = 2*(precision * recall  /(precision + recall))

	print("evaluation of file " + fileName)
	print("accuracy: " + str(acc))
	print("precision: " + str(precision))
	print("recall: " + str(recall))
	print("f1: " + str(f1) )
	#raw_input()
	return (acc, precision, recall, f1)