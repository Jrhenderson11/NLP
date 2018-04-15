#!/usr/env/bin python3
import pprint
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

def get_sample_data():
	nb_samples = 1000
	X, _ = make_blobs(n_samples=nb_samples, n_features=5, centers=7, cluster_std=1.5)
	print("generated random data")
	return X

def plot_clusters(data, clust_labels, clust_cents):
	print("Plotting clusters")
	#clust_labels, cent = doKmeans(wh1, 2)
	kmeans = pd.DataFrame(clust_labels)
	#wh1.insert((wh1.shape[1]),'kmeans',kmeans)
	#Plot the clusters obtained using k means
	fig = plt.figure()
	ax = fig.add_subplot(111)
	scatter = ax.scatter([x[0] for x in data], [x[1] for x in data], c=kmeans[0],s=50)
	ax.set_title('Clustering visualisation')
	plt.colorbar(scatter)
	plt.show()


def plot_data(data):
	print("Plotting data")
	plt.plot([x[0] for x in data], [x[1] for x in data], 'ro', k_means_test(X))
	plt.show()

def calculate_euclidian_vector_distance_normalized(v1, v2):
	#transform sparse matrix to array
	print("calculating distance")
	delta = v1 - v2
	print(sp.linalg.norm(delta.toarray()))
	return sp.linalg.norm(delta.toarray())

def k_means_test(X):
	print("ca")
	km = KMeans(n_clusters=3)
	#KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300, n_clusters=3, n_init=10, n_jobs=1, precompute_distances='auto', random_state=None, tol=0.0001, verbose=0)
	km.fit(X)
	clust_labels = km.predict(X)
	clust_cents = km.cluster_centers_
	return (clust_labels, clust_cents)

if __name__ == "__main__":
	X = get_sample_data()
	#pprint.pprint(X)
	#print(type(X))
	#plot_data(X)
	(clust_labels, clust_cents) = k_means_test(X)
	plot_clusters(X, clust_labels, clust_cents)