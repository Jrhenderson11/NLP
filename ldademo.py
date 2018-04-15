#!/usr/bin/env python3
from pprint import pprint
from gensim import corpora, models
from matplotlib import pyplot as plt

#cd data; wget http://www.cs.columbia.edu/~blei/lda-c/ap.tgz; tar -xvf ap.tgz
corpus = corpora.BleiCorpus('./data/ap/ap.dat', './data/ap/vocab.txt')

print("building model")
#model = models.ldamodel.LdaModel(corpus, num_topics=100, id2word=corpus.id2word, alpha=1)
model = models.ldamodel.LdaModel(corpus, num_topics=100, id2word=corpus.id2word)
print("done!")
doc = corpus.docbyoffset(0)
topics = model[doc]
#topics is list of pairs: (index, weight)
print(topics)

# display histogram
num_topics_used = [len(model[doc]) for doc in corpus]
plt.title("Histogram ")
plt.hist(num_topics_used)
plt.show()

#input()