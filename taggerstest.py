import nltk

from nltk.corpus import brown
from nltk.corpus import treebank
from nltk.tag import DefaultTagger


def backoff_tagger(training, tagger_classes, backoff=None):
	for cls in tagger_classes :
	      backoff = cls(train_sents, backoff=backoff)
	return backoff

def train_brill_tagger(initial_tagger, train_sents, **kwargs):
	templates = [brill.Template(brill.Pos([-1])),
	brill.Template(brill.Pos([1])),
	brill.Template(brill.Pos([-2])),
	brill.Template(brill.Pos([2])),
	brill.Template(brill.Pos([-2, -1])),
	brill.Template(brill.Pos([1, 2])),
	brill.Template(brill.Pos([-3, -2, -1])),
	brill.Template(brill.Pos([1, 2, 3])),
	brill.Template(brill.Pos([-1]), brill.Pos([1])),
	brill.Template(brill.Word([-1])),
	brill.Template(brill.Word([1])),
	brill.Template(brill.Word([-2])),
	brill.Template(brill.Word([2])),
	brill.Template(brill.Word([-2, -1])),
	brill.Template(brill.Word([1, 2])),
	brill.Template(brill.Word([-3, -2, -1])),
	brill.Template(brill.Word([1, 2, 3])),
	brill.Template(brill.Word([-1]), brill.Word([1])),]
	trainer = brill_trainer.BrillTaggerTrainer(initial_tagger, templates, deterministic=True)
	return trainer.train(train_sents, **kwargs)


training = treebank.tagged_sents()[0:3500] 
testing = treebank.tagged_sents()[3500:]
print(len(treebank.tagged_sents()))
#tagger = DefaultTagger('NN')


#-----------------------------------------------------

from nltk.tag import UnigramTagger

unigramTagger = UnigramTagger(training, cutoff=2)
# same as tagger.train(training)


print('Uniigram tagger accuracy:')
print(unigramTagger.evaluate(testing))



#-----------------------------------------------------

print('Bigram tagger accuracy:')

from nltk.tag import BigramTagger

bigramTagger = BigramTagger(training)

print(bigramTagger.evaluate(testing))

#-----------------------------------------------------
print('Trigram tagger accuracy:')

from nltk.tag import TrigramTagger
trigramTagger = TrigramTagger(training)

print(trigramTagger.evaluate(testing))
#-----------------------------------------------------

#Brill Tagger
from nltk.tag import brill, brill_trainer
# make sure you've got some train_sents!
#brill_tagger = train_brill_tagger(unigramTagger, training)

print('Brill tagger accuracy:')
#print(brill_tagger.evaluate(testing))

#------------------------------------------------------

#			Backoff tagger



#bigram_tagger = BigramTagger(training, backoff=unigramTagger)

#Here is some code for making it a little easier to use backoff for an ensemble of taggers.


#tagger = backoff_tagger(training, [UnigramTagger, BigramTagger, TrigramTagger], backoff=DefaultTagger('NN'))


#-------------------------------------------------------

#			TESTER

print('beginning test')

#test cutoffs for different algorithms and 
from collections import Counter

counter = {}


#mix datasets
for split in range(100, 3900, 100):

	counter = {}

	training = treebank.tagged_sents()[0:split] 
	testing = treebank.tagged_sents()[split:]

	print("=================================")
	print("split = " + str(split))
	for i in xrange(0,10):

		name = 'u' + str(i)
		tagger = UnigramTagger(training, cutoff=i)
		#counter[name] = tagger.evaluate(testing)
		counter[tagger.evaluate(testing)] = name
		#print(counter[name])
		name = 'b' + str(i)
		tagger = BigramTagger(training, cutoff=i)
		counter[tagger.evaluate(testing)] = name
		name = 't' + str(i)
		tagger = TrigramTagger(training, cutoff=i)
	#	counter[name] = tagger.evaluate(testing)
		counter[tagger.evaluate(testing)] = name


	for x in (sorted(counter.items())):
		print x
















