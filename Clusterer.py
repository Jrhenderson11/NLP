#!/usr/env/bin python3
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

def get_sample_data():
	nb_samples = 1000
	X, _ = make_blobs(n_samples=nb_samples, n_features=20, centers=7, cluster_std=1.5)
	print("generated random data")
	return X

def plot_clusters(data, clust_labels, clust_cents):
	#sp.linalg.norm(delta.toarray())
	print("Plotting clusters")
	kmeans = pd.DataFrame(clust_labels)
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

def plot_cluster_v_inertia(X, min_clusters, max_clusters):
	print("calculating cluster vs inertia graph for "+ str(min_clusters)+"-" + str(max_clusters)+" (may take a while)")
	inertias = []
	for i in range(min_clusters, max(len(X), max_clusters)):
		inertias.append((kmeans_cluster(X, num_clusters=i)[2]))
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_xlabel('Number of clusters')
	ax.set_ylabel('Inertia')
	ax.set_title("Clusters vs Inertia")
	#plt.T
	plt.plot(inertias)
	plt.show()

def calculate_euclidian_vector_distance_normalized(v1, v2):
	#transform sparse matrix to array
	print("calculating distance")
	delta = v1 - v2
	print(sp.linalg.norm(delta.toarray()))
	return sp.linalg.norm(delta.toarray())

def kmeans_cluster(X, num_clusters=3):
	#print("clustering")
	#pprint(X)
	km = KMeans(n_clusters=num_clusters, init='k-means++')
	#KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300, n_clusters=3, n_init=10, n_jobs=1, precompute_distances='auto', random_state=None, tol=0.0001, verbose=0)
	km.fit(X)
	#predict with km.predict(vector) to return cluster label
	clust_labels = km.predict(X)
	clust_cents = km.cluster_centers_

	return (clust_labels, clust_cents, km.inertia_, km)

def get_km_model(X, num_clusters=3):
	km = KMeans(n_clusters=num_clusters, init='k-means++')
	#KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300, n_clusters=3, n_init=10, n_jobs=1, precompute_distances='auto', random_state=None, tol=0.0001, verbose=0)
	km.fit(X)
	#predict with km.predict(vector) to return cluster label
	clust_labels = km.predict(X)
	clust_cents = km.cluster_centers_	
	return km

if __name__ == "__main__":
	X = get_sample_data()
	#pprint.pprint(X)
	#print(type(X))
	#plot_data(X)
	(clust_labels, clust_cents) = kmeans_cluster(X)
	plot_clusters(X, clust_labels, clust_cents)



''' EXAMPLE
>>> from sklearn.cluster import KMeans
>>> import numpy as np
>>> X = np.array([[1, 2], [1, 4], [1, 0],
...               [4, 2], [4, 4], [4, 0]])
>>> kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
>>> kmeans.labels_
array([0, 0, 0, 1, 1, 1], dtype=int32)
>>> kmeans.predict([[0, 0], [4, 4]])
array([0, 1], dtype=int32)
>>> kmeans.cluster_centers_
array([[ 1.,  2.],
       [ 4.,  2.]])
'''