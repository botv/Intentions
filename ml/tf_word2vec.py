import numpy as np #Matrix Math
import tensorflow as tf #Api for building models
import pandas as pd #Loading data
import pickle
from copy import deepcopy
from string import punctuation
from random import shuffle

from tqdm import tqdm #Progress of df creation
tqdm.pandas(desc="progress-bar")

from nltk.tokenize import TweetTokenizer # a tweet tokenizer from nltk.
tokenizer = TweetTokenizer()

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

class process(object):

	def __init__(self, windowSize, mode):
		self.windowSize = windowSize
		self.mode = mode
		self.vocabSize = 0

	def ingest(self):
		data = pd.read_csv('./data/text_emotion.csv')
		data.drop(['tweet_id','author'], axis=1, inplace = True)
		data = data[data.sentiment.isnull() == False]
		data = data[data['content'].isnull() == False]
		data.reset_index(inplace = True)
		data.drop('index', axis=1, inplace = True)
		print('dataset loaded with shape:', data.shape)
		dfContent = data.content
		content = [x for x in dfContent]
		dfSentiment = data.sentiment
		sentiment = [x for x in dfSentiment]
		length = len(data.content)
		return data, content, sentiment, length

	def tokenize(self,tweet):
		try:
			tokens = tokenizer.tokenize(tweet.lower())
			tokens = [x for x in tokens if not x.startswith('@')]
			tokens = [x for x in tokens if not x.startswith('#')]
			tokens = [x for x in tokens if not x.startswith('http')]
			tokens = [x for x in tokens if not x.startswith('www')]
			return tokens
		except:
			return('NC')

	def postProcess(self,tweets):
		tweets = [self.tokenize(tweet) for tweet in tweets if not tweet == 'NC']
		return tweets

	def getDicts(self,tweets):
		vocab = []
		for tweet in tweets:
			for word in tweet:
				if word not in vocab:
					vocab.append(word)
		vocabSize = len(vocab)
		word2int = {}
		int2word = {}

		for i,word in enumerate(vocab):
			word2int[word] = i
			int2word[i] = word
		return vocabSize, word2int, int2word

	def wordPairs(self,windowSize, tweets):
		data = []
		for tweet in tweets:
			for index,word in enumerate(tweet):
				for nbWord in tweet[max(index - windowSize, 0):
					min(index+windowSize,len(tweet))+1]:
					if nbWord != word:
						data.append([word,nbWord])
		return data

	def oneHot(self, dpi, vocabSize):
		temp = np.zeros(vocabSize)
		temp[dpi] = 1
		return temp

	def createTrain(self,pairs, vocabSize, word2int, int2word):
		x_train = []
		y_train = []
		for pairWord in pairs:
			x_train.append(self.oneHot(word2int[pairWord[0]],vocabSize))
			y_train.append(self.oneHot(word2int[pairWord[1]],vocabSize))
		return np.asarray(x_train), np.asarray(y_train)

	def writeToMemory(self, data, length, processed):
		if processed:
			x_train = data[0]
			print(x_train[0])
			y_train = data[1]
			print(y_train[0])
			np.save('./data/processed/x_train_%s'%(length),x_train)
			np.save('./data/processed/y_train_%s'%(length),y_train)
		else:
			for fileIndex in range(0,int(length/500)):
				np.save('./data/process_%s'%(fileIndex),data[(fileIndex*500):((fileIndex+1)*500)])


	def saveDicts(self, word2int, int2word, vocabSize, length):
		np.save('./data/vocabSize', vocabSize)
		np.save('./data/length', length)
		with open('./data/word2int.pickle','wb') as f:
			pickle.dump(word2int,f,protocol=pickle.HIGHEST_PROTOCOL)
		with open('./data/int2word.pickle', 'wb') as f:
			pickle.dump(int2word,f,protocol=pickle.HIGHEST_PROTOCOL)

	def processFromMemory(self,length,vocabSize, word2int, int2word):
		for fileIndex in range(0,int(length/500)):
			with open('./data/process_%s.npy'%(fileIndex), 'rb') as f:
				tweets = np.load(f)
				data = self.wordPairs(self.windowSize, tweets)
				x_train, y_train = self.createTrain(data,vocabSize, word2int, int2word)
				data = [x_train,y_train]
				self.writeToMemory(data, fileIndex, True)



	def main(self):
		if self.mode:
			data, tweets, sentiments, length = self.ingest();
			tweets = self.postProcess(tweets)
			vocabSize, word2int, int2word = self.getDicts(tweets)
			self.writeToMemory(tweets, length, False)
			self.saveDicts(word2int,int2word,vocabSize,length)
		else:
			vocabSize = np.load('./data/vocabSize.npy')
			length = np.load('./data/length.npy')
			word2int = np.load('./data/word2int.pickle')
			int2word = np.load('./data/int2word.pickle')
			self.processFromMemory(length, vocabSize, word2int, int2word)


process = process(2,False)
process.main()