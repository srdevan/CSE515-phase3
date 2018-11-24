from util import Util
from collections import OrderedDict
import numpy as np
import pandas as pd
import constants
from data_extractor import DataExtractor
from sklearn.preprocessing import MinMaxScaler
import pickle

class Task6a():
	def __init__(self):
		self.ut = Util()
		self.img_ids = []
		self.adj_matrix = []
		self.img_feature_matrix = []
		self.label_img_matrix = dict()
		self.input_image_label_pairs = OrderedDict()

	def generate_img_img_adj_matrix(self):
		""" Method: generate image-image similarity matrix and stash in pickle file"""
		print("getting and normalizing data...")
		data_extractor = DataExtractor()
		loc_mapping = data_extractor.location_mapping()
		self.img_feature_matrix = data_extractor.prepare_dataset_for_task6(loc_mapping)
		scaler = MinMaxScaler()
		scaler.fit(list(self.img_feature_matrix.values()))
		for img, feature in self.img_feature_matrix.items():
			self.img_feature_matrix[img] = scaler.transform([feature])[0]
		self.img_ids = list(self.img_feature_matrix.keys())

	def get_img_img_adj_matrix(self):
		""" Method: read image-image similarity matrix from pickle file"""
		with open('adj_mat_6a.pickle', 'rb') as file_handle:
			self.adj_matrix = pickle.load(file_handle)

	def get_euclidean_similarity(self, features_image1, features_image2):
		""" Method: image-image similarity computation"""
		return self.ut.compute_euclidean_distance(np.array(features_image1), np.array(features_image2))

	def read_input_labels_pairs(self):
		""" Method: read input image-label pairs"""
		input_image_label_pairs_df = pd.read_csv('../input/task_6a.txt')
		input_images = list(input_image_label_pairs_df['image'])
		input_labels = list(input_image_label_pairs_df['label'])
		self.input_image_label_pairs = OrderedDict(zip(input_images, input_labels))
		for i in range(0, len(input_labels)):
			if input_labels[i] in self.label_img_matrix:
				self.label_img_matrix[input_labels[i]].append([input_images[i],0])
			else:
				self.label_img_matrix[input_labels[i]] = [[input_images[i],0]]

	def classify_images(self, k):
		""" Method: Classify all images based on given image-label pairs"""
		labelled_image_ids = list(self.input_image_label_pairs.keys())
		input_image_labels = list(self.input_image_label_pairs.values())
		for image in self.img_ids:
			label_similarity_dict = dict()
			for i, labelled_image in enumerate(labelled_image_ids):
				if input_image_labels[i] in label_similarity_dict:
					label_similarity_dict[input_image_labels[i]] += self.get_euclidean_similarity(self.img_feature_matrix[str(image)], self.img_feature_matrix[str(labelled_image)])
				else:
					label_similarity_dict[input_image_labels[i]] = self.get_euclidean_similarity(self.img_feature_matrix[str(image)], self.img_feature_matrix[str(labelled_image)])
			for label in label_similarity_dict:
				label_similarity_dict[label] = label_similarity_dict[label]/input_image_labels.count(label)
			min_sim = min(label_similarity_dict.values())
			for label, sim in label_similarity_dict.items():
				if sim == min_sim:
					self.label_img_matrix[label].append([image, sim])

	def pretty_print(self):
		""" Method: Print all image label pairs onto html file for visualization"""
		op = open(constants.TASK6a_OUTPUT_FILE, "w")
		image_ids_seen = []
		for label, image_ids in self.label_img_matrix.items():
			op.write("Label " + label + "\n")
			image_ids.sort(key=lambda x: x[1])
			for temp in image_ids:
				if temp[0] not in image_ids_seen:
					op.write(str(temp[0]) + "\n")
					image_ids_seen.append(temp[0])
			op.write("####\n")
		
if __name__ == "__main__":
	task = Task6a()
	k = input('Enter value of k:')
	task.generate_img_img_adj_matrix()
	task.read_input_labels_pairs()
	task.classify_images(k)
	task.pretty_print()
