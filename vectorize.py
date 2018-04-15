from gensim import corpora

texts = [["word1", "w2", "apple"],["word2", "pear", "word1"]]
dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/deerwester.dict')  # store the dictionary, for future reference
print(dictionary)
#Dictionary(12 unique tokens)
print(dictionary.token2id)

#convert doc to vec
new_doc = "Human computer interaction"
new_vec = dictionary.doc2bow(new_doc.lower().split())

#do for whole corpus
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/tmp/deerwester.mm', corpus)  # store to disk, for later use
print(corpus)
