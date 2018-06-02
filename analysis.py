import Ontology
from gensim import corpora
from sklearn.datasets import fetch_20newsgroups
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

def unsparsify(vector_list, dimension):
	unsparse = []
	value_dict = dict()
	for (k,v) in vector_list:
		value_dict[k] = v
	for i in range(dimension):
		if i in value_dict:
			unsparse.append(value_dict[i])
		else:
			unsparse.append(0)
	return unsparse

# given a list of files and produces a dictionary of keywords used to identify the topic
def get_keywords_dict(fileList):
	print("generating keywords dictionary")
	# keywords dict will be a dictionary of filenames and topic keywords
	keywords_dict = dict()
	for file in fileList:
		f = open(file, 'r')
		text = f.read()
		f.close()

		topicwords = Ontology.get_topic(text)
		keywords_dict[file] = topicwords
	print("done")
	return keywords_dict

# is given a fileList and returns a dictionary with relevant (sparse) tf-idf vectors 
def generate_tfidf_matrix_batch(fileList):
	print("generating tf-dif matrix for " + str(len(fileList)) + " files")
	#get initial dictionary, to provide list to generate tf-idf matrix
	input_dict = get_keywords_dict(fileList)

	total_words = []
	for fileName in input_dict:
		total_words.append(input_dict[fileName].split(" "))

	dictionary = corpora.Dictionary(total_words)
	#dictionary.save('bagofwords')  # store the dictionary, for future reference

	vector_dict = dict()
	for fileName in input_dict:
		new_vec = dictionary.doc2bow(input_dict[fileName].lower().split())
		vector_dict[fileName] = new_vec

	return vector_dict, len(dictionary)

# Demo code (DOESNT WORK BECAUSE JUST SOME PLACEHOLDER STUFF)
def naive_bayes(input_data):

	#Define the map of categories that will be used for training. We will be using five categories
	#in this case. The keys in this dictionary object refer to the names in the scikit-learn dataset.
	category_map = {'talk.politics.misc': 'Politics', 'rec.autos': 'Autos', 'rec.sport.hockey': 'Hockey', 'sci.electronics': 'Electronics', 'sci.med': 'Medicine'}

	# Get the training dataset
	training_data = fetch_20newsgroups(subset='train', categories=category_map.keys(), shuffle=True, random_state=5)

	# Build a count vectorizer and extract term counts
	count_vectorizer = CountVectorizer()
	train_tc = count_vectorizer.fit_transform(training_data.data)
	print("\nDimensions of training data:", train_tc.shape)

	# Create the tf-idf transformer
	tfidf = TfidfTransformer()
	train_tfidf = tfidf.fit_transform(train_tc)

	# Train a Multinomial Naive Bayes classifier
	classifier = MultinomialNB().fit(train_tfidf, training_data.target)

	# Transform input data using count vectorizer
	input_tc = count_vectorizer.transform(input_data)

	# Transform vectorized data using tfidf transformer
	input_tfidf = tfidf.transform(input_tc)

	# Predict the output categories
	predictions = classifier.predict(input_tfidf)

	# Print the outputs
	for sent, category in zip(input_data, predictions):
		print('\nInput:', sent, '\nPredicted category:', category_map[training_data.target_names[category]])

# yeah this doesn't work either (check out ldademo.py tho)
def latent_dirichlet_allocation():
	print("do STUFF")
