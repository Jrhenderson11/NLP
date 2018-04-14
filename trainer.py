import re
import os
import nltk
import Code
import pickle
import string
from os import listdir
from nltk.corpus import brown
from nltk.corpus import treebank
from nltk.tag import DefaultTagger
from nltk.tag import UnigramTagger, BigramTagger, TrigramTagger
from os.path import isfile, join, dirname


def backoff_tagger(training, tagger_classes, backoff=None):
	for cls in tagger_classes :
	      backoff = cls(training, backoff=backoff)
	return backoff


#train tagger once for entire batch of files to speed things up a little
training = treebank.tagged_sents()
#unigramTagger = UnigramTagger(training, DefaultTagger('NN'))
#bigramtagger = BigramTagger(training)
#trigramTagger = TrigramTagger(training)
#backbitagger = BigramTagger(training, backoff=unigramTagger)
#tagger = TrigramTagger(training, backoff=backbitagger)

tagger = TrigramTagger(training)




#tagger = backoff_tagger(training, [UnigramTagger, BigramTagger, TrigramTagger], backoff=DefaultTagger('NN'))

saver = open("postagger.pickle","wb")
pickle.dump(tagger, saver)
saver.close()
print "done"