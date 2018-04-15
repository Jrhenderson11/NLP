import Ontology
from sklearn.datasets import fetch_20newsgroups
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

def get_keywords_dict(fileList):
	# keywords dict will be a dictionary of filenames and topic keywords
	keywords_dict = dict()
	for file in fileList:
		f = open(fname, 'r')
		text = f.read()
		f.close()

		topicwords = Ontology.get_topic(text)
		keywords_dict[file] = topicwords
	return keywords_dict

def generate_tfidf_matrix_batch(fileList):
	#get initial dictionary, to provide list to generate tf-idf matrix
	input_dict = get_keywords_dict(fileList)

	print(input_dict.values)

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


def latent_dirichlet_allocation():
	print("do STUFF")
