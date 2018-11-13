"""
This module contains all functions used throughout the codebase.
"""
import constants
import numpy as np
import pickle
from sklearn.decomposition import TruncatedSVD

class Util():

	def __init__(self):
		pass

	""" Returns the euclidean distance between vector_one and vetor_two """
	def compute_euclidean_distance(self, vector_one, vector_two):
		return np.linalg.norm(vector_one - vector_two)

	def fetch_imgximg_graph(self):
		"""
		1. load pickle file and return the graph stored.
		"""
		pass

	def fetch_dict_graph(self):
		"""
		graph returned in this format -
		graph = [{(1,2): 0.8, (1,3): 0.7, ....},
				{(2,1): 0.8, (2,3): 0.75, ...}]
		"""
		pass

	def image_id_mapping(self):
		image_id_mapping_file = open(constants.DUMPED_OBJECTS_DIR_PATH + "image_id_mapping.pickle", "rb")
		return pickle.load(image_id_mapping_file)[0][1]

	def dim_reduce_SVD(self, input_arr, k):
		svd = TruncatedSVD(n_components=int(k))
		svd.fit(input_arr)

		return(svd.transform(input_arr))
