import nltk

from nltk.corpus import brown
from nltk.corpus.reader import WordListCorpusReader
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer

x = nltk.data.load('files/big.txt', format='text')

reader = WordListCorpusReader('files/', ['computerscience.txt'])
cs_text = reader.raw()
cs_words = []

cs_words = (nltk.word_tokenize(cs_text))

print(cs_words)

stemmer = PorterStemmer()
wnl = WordNetLemmatizer()

for word in cs_words:
	print(stemmer.stem(word))
	print(wnl.lemmatize(word))



