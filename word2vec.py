import gensim
from gensim.models import Word2Vec

model = gensim.models.KeyedVectors.load_word2vec_format('files/GoogleNews-vectors-negative300.bin', binary=True)

#get dimensionality? model for word
#model['word']


#get similarity = 
#model.similarity(w1, w2)
#l =[ ([ 'woman', 'king'], ['man']), (['woman', 'uncle'],['man']), (['cats', 'puppies'],['dogs']), (['train', 'roads'], ['car'])]
#for (p,n) in l:
#	print(model.most_similar(positive=p, negative=n))
print "=========="
#
	
	
	
#print model.similarity('mirror physics Markov Random Fields', 'physics')
if 'sdafdad' in model.wv.vocab:
	print model.similarity('Physics', 'sdafdad')
else:	
	print "not found"
print model.similarity('Physics', 'Physics')
print model.similarity('Physics', 'physics')
print model.similarity('Physics', 'apple')

	
#print (model.doesnt_match( ["GSIA 259", "5000 Forbes Avenue", "Simon Graduate School", "Carnegie Mellon University", "Graduate School", "Business Administration"] ))
#print (model.doesnt_match( ["Paris", "London", "Berlin", "Italy"] ))