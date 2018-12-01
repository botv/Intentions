import pandas as pd 
import numpy as np 
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelBinarizer
import html
import nltk


class pre_process(object):

	def __init__(self, csv_dir, content_dir, sentiment_dir):
		self.csv_dir = csv_dir
		self.tokenizer = RegexpTokenizer(r'\w+')
		self.content_dir = content_dir
		self.sentiment_dir = sentiment_dir


	def process(self):
		df = pd.read_csv(self.csv_dir)
		sentiment = df['sentiment'].values
		content = df['content'].values
		counter = 0
		for c in content:
			content[counter] = html.unescape(c)
			counter += 1
		counter = 0
		for c in content:
			content[counter] = self.tokenizer.tokenize(content[counter])
			counter += 1
		X = list(content)
		dictionary = self.enumerate(X)
		for i, sentence in enumerate(content):
			for j, word in enumerate(sentence):
				content[i][j] = dictionary.get(word)
		content = self.pad(content)
		content = np.asarray(content)
		sentiment = self.binarize(sentiment)
		np.save(self.content_dir, content)
		np.save(self.sentiment_dir, sentiment)
		
		
	def enumerate(self, sentences):
		words = []
		for sentence in sentences:
			for word in sentence:
				words.append(word)

		unique = list(set(words))
		dictionary = {}
		for index, word in enumerate(unique):
			dictionary.update({word:index+1})
		return dictionary


	def pad(self, sentences):
		sentences = pad_sequences(sequences =sentences , padding='pre', truncating='pre', maxlen = 150)
		return sentences

	def binarize(self, labels):
		lb = LabelBinarizer()
		labels = lb.fit_transform(np.asarray(labels))
		return labels


processor = pre_process('text_emotion.csv', 'content.npy', 'sentiment.npy')
processor.process()
