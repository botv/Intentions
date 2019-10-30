import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
import os

def build_dataset():
	DIRECTORY_URL = 'https://storage.googleapis.com/download.tensorflow.org/data/illiad/'
	FILE_NAMES = ['cowper.txt', 'derby.txt', 'butler.txt']

	for name in FILE_NAMES:
		text_dir = tf.keras.utils.get_file(name, origin=DIRECTORY_URL+name)
	  
	parent_dir = os.path.dirname(text_dir)

	def labeler(example, index):
 		return example, tf.cast(index, tf.int64)  

	labeled_data_sets = []

	for i, file_name in enumerate(FILE_NAMES):
		lines_dataset = tf.data.TextLineDataset(os.path.join(parent_dir, file_name))
		labeled_dataset = lines_dataset.map(lambda ex: labeler(ex, i))
		labeled_data_sets.append(labeled_dataset)

	BUFFER_SIZE = 50000
	BATCH_SIZE = 64
	TAKE_SIZE = 5000

	all_labeled_data = labeled_data_sets[0]
	for labeled_dataset in labeled_data_sets[1:]:
		all_labeled_data = all_labeled_data.concatenate(labeled_dataset)
  
	all_labeled_data = all_labeled_data.shuffle(
    	BUFFER_SIZE, reshuffle_each_iteration=False)

	tokenizer = tfds.features.text.Tokenizer()

	vocabulary_set = set()
	for text_tensor, _ in all_labeled_data:
		some_tokens = tokenizer.tokenize(text_tensor.numpy())
		vocabulary_set.update(some_tokens)

	vocab_size = len(vocabulary_set)
	encoder = tfds.features.text.TokenTextEncoder(vocabulary_set)
		
	sample_one_hot = np.zeros(3)		

	def encode(text_tensor, label):
		encoded_text = encoder.encode(text_tensor.numpy())
		label_hot = np.zeros(3)
		label_hot[label-1] = 1
		return encoded_text, label_hot

	def encode_map_fn(text, label):
		return tf.py_function(encode, inp=[text, label], Tout=(tf.int64, tf.int64))

	all_encoded_data = all_labeled_data.map(encode_map_fn)

	train_data = all_encoded_data.skip(TAKE_SIZE).shuffle(BUFFER_SIZE)
	train_data = train_data.padded_batch(BATCH_SIZE, padded_shapes=([-1],[-1]))
	test_data = all_encoded_data.take(TAKE_SIZE)
	test_data = test_data.padded_batch(BATCH_SIZE, padded_shapes=([-1],[-1]))

	vocab_size += 1

	sample_text, sample_labels = next(iter(test_data))

	return train_data, test_data, vocab_size


build_dataset()
