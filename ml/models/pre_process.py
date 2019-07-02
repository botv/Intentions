import tensorflow as tf
import tensorflow_datasets as tfds
import os
import pandas as pd
import numpy as np
import string
import nltk
import pickle
from nltk.corpus import stopwords
#from gensim.models import Word2Vec
import re

class Pre_Process(object):

	def __init__(
			self, text_dir, chunk_size, processed_input_dir, processed_label_dir,
			BUFFER_SIZE, BATCH_SIZE, TAKE_SIZE
			):
		self.text_dir = text_dir
		self.chunk_size = chunk_size
		self.processed_input_dir = processed_input_dir
		self.processed_label_dir = processed_label_dir
		self.BUFFER_SIZE = BUFFER_SIZE
		self.BATCH_SIZE = BATCH_SIZE
		self.TAKE_SIZE = TAKE_SIZE


	def clean_text(self):
		for index,chunk in enumerate(pd.read_csv(
				self.text_dir,chunksize=self.chunk_size)):
			for content, label in zip(chunk['content'], chunk['sentiment']):
				processed_text = content.lower()
				processed_text = re.sub(r'\d+', '', processed_text)
				processed_text = processed_text.translate(
					str.maketrans('', '', string.punctuation)
					)
				processed_text = processed_text.strip()
				processed_text = nltk.word_tokenize(processed_text)
				processed_text = ' '.join([str(w) for w in processed_text])
				with open(self.processed_input_dir, 'a') as pid:
					pid.write(processed_text + '\n')
				with open(self.processed_label_dir, 'a') as pld:
					pld.write(label + '\n')

	
	def build_dataset(self):
		content_dataset = tf.data.TextLineDataset(self.processed_input_dir)
		sentiment_dataset = tf.data.TextLineDataset(self.processed_label_dir)

		data = tf.data.Dataset.zip((content_dataset,sentiment_dataset))
		data = data.shuffle(
				self.BUFFER_SIZE,
				)

		tokenizer = tfds.features.text.Tokenizer()

		content_vocab = set()
		sentiment_vocab = set()
		for content_tensor, sentiment_tensor in data:
			content_tokens = tokenizer.tokenize(content_tensor.numpy())
			sentiment_tokens = tokenizer.tokenize(sentiment_tensor.numpy())
			content_vocab.update(content_tokens)
			sentiment_vocab.update(sentiment_tokens)

		vocab_size = len(content_vocab) + 1
		label_size = len(sentiment_vocab)

		sample_one_hot = np.zeros(label_size)		
		
		content_encoder = tfds.features.text.TokenTextEncoder(content_vocab)
		sentiment_encoder = tfds.features.text.TokenTextEncoder(sentiment_vocab)

		def encode(content_tensor,label_tensor):
			encoded_content = content_encoder.encode(content_tensor.numpy())
			encoded_label = sentiment_encoder.encode(label_tensor.numpy())[0]
			one_hot_label = sample_one_hot
			one_hot_label[encoded_label - 1] = 1
			return encoded_content, one_hot_label

		def encode_map_fn(text, label):
  			return tf.py_function(encode, inp=[text, label], Tout=(tf.int64, tf.int64))

		data = data.map(encode_map_fn)

		train_data = data.skip(self.TAKE_SIZE).shuffle(self.BUFFER_SIZE)
		train_data = train_data.padded_batch(self.BATCH_SIZE, padded_shapes=([-1],[-1]))

		test_data = data.take(self.TAKE_SIZE)
		test_data = test_data.padded_batch(self.BATCH_SIZE, padded_shapes=([-1],[-1]))

		return train_data, test_data, vocab_size, label_size
#if __name__ == '__main__':
	# p = Pre_Process(
	# 	'../data/text_emotion.csv', 5000,
	# 	'../data/content.txt', '../data/label.txt',
	# 	40000, 10000, 5000
	# )
	# p.clean_text()
	#p.build_dataset()
	#content_dict,sentiment_dict = p.retrieve_vocab()
	#p.enumerate(content_dict,sentiment_dict)
