import tensorflow as tf
import pandas as pd
import numpy as np
import string
import nltk
from nltk.corpus import stopwords
from gensim.models import Word2Vec
import re

class Pre_Process(object):

	def __init__(
			self,training_threads,text_dir,chunk_size,
			processed_input_dir, processed_label_dir
		):
		self.training_threads = training_threads
		self.text_dir = text_dir
		self.chunk_size = chunk_size
		self.processed_input_dir = processed_input_dir
		self.processed_label_dir = processed_label_dir


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
				label = label
				with open(self.processed_input_dir, 'a') as pid:
					pid.write(processed_text + '\n')
				with open(self.processed_label_dir, 'a') as pld:
					pld.write(label + '\n')


	def retrieve_vocab(self):
		unique_sentiments = []
		unique_content = []
		one_hot_ref = {}
		with open(self.processed_label_dir, 'r') as pld:
			for label in pld:
				l = label[0:-1]
				if l not in unique_sentiments:
					unique_sentiments.append(l)
		with open(self.processed_input_dir, 'r') as pid:
			for sentence in pid:
				s = nltk.word_tokenize(sentence)
				for i in range(len(s)):
					s[i] = [w for w in s[i] if w not in stopwords.words('english')]
				for w in s:
					if w not in unique_content:
						unique_content.append(w)
		for i, us in enumerate(unique_sentiments):
			one_hot_sent[us] = i
		for i, uc in enumerate(unique_content):
			one_hot_cont[uc] = i
		return one_hot_cont, one_hot_sent

	def save_as_array(self,one_hot_sentiment):
		complete_content = []
		complete_labels = []
		with open(self.processed_input_dir,'r') as pid:
			for sentence in pid:
				s = nltk.word_tokenize(sentence)
				for i in range(len(s)):
					s[i] = [w for w in s[i] if w not in stopwords.words('english')]
				complete_content.append(s)
		with open(self.processed_label_dir,'r') as pld:
			for label in pld:
				complete_labels.append(one_hot_sentiment[label[0:-1]])



if __name__ == '__main__':
	p = Pre_Process(
		2,'../data/text_emotion.csv',5000,
		'../data/content.txt', '../data/label.txt'
	)
	p.clean_text()
	one_hot_content,one_hot_sentiment = p.retrieve_sentiment_vocab()
	p.save_as_array(one_hot_sentiment)
