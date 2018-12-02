import tensorflow as tf
import keras
from keras.utils import to_categorical
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Embedding
from keras.layers import Flatten
from keras.callbacks import ModelCheckpoint
from keras.callbacks import TensorBoard
from keras import regularizers
from keras import backend as KTF
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd


class model(object):
	def __init__(self, lstm_size, dropout, batch_size, epochs):
		self.X = np.load('../data/tweet.npy')
		self.Y = np.load('../data/output.npy')
		self.X = self.X[:200000]
		self.Y = self.Y[:200000]
		self.lstm_size = lstm_size
		self.dropout = dropout
		self.batch_size = batch_size
		self.epochs = epochs
		self.train_X, self.val_X, self.train_Y, self.val_Y = train_test_split(self.X, self.Y, test_size=0.5)
		self.n_words = 791771

	def model_architecture(self):
		print('----------- Running Lstm ------------')
		model = Sequential()
		model.add(Embedding(self.n_words + 1, 200, input_length=5))
		model.add(LSTM(self.lstm_size, return_sequences=True))
		model.add(LSTM(self.lstm_size, return_sequences=True))
		model.add(Dropout(self.dropout))
		model.add(Flatten())
		model.add(Dense(self.n_words, activation='softmax', kernel_regularizer=regularizers.l2(0.01)))
		model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
		tensorboard = TensorBoard(log_dir="logs/{}", histogram_freq=0, batch_size=self.batch_size, write_graph=False,
		                          write_grads=False, write_images=False, embeddings_freq=0, embeddings_layer_names=None,
		                          embeddings_metadata=None)

		filepath = 'checkpoints/pred_model.hdf5'

		checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=False, mode='min')
		model.fit(self.train_X, self.train_Y, epochs=self.epochs, batch_size=self.batch_size,
		          callbacks=[checkpoint, tensorboard], validation_data=(self.val_X, self.val_Y))


model = model(20, 0.5, 1000, 100)
model.model_architecture()
