import tensorflow as tf 
from tensorflow.keras.layers import (
	Dense,
	LSTM,
	Embedding,
	Bidirectional,
	BatchNormalization
	)
from tensorflow.keras import Model
import numpy as np

from p2 import *

import pre_process

tf.keras.backend.clear_session()

p = pre_process.Pre_Process('../data/text_emotion.csv', 1,
	'../data/content.txt', '../data/label.txt',40000, 5000, 5000)

train_ds, test_ds, VOCAB_SIZE, LABEL_SIZE = p.build_dataset()

EMBEDDING_DIM = 64
#NUM_FATURES =
SAVE_PATH = '../saved_models/sentiment_analysis_model'
EPOCHS = 1000
LSTM_CELLS_1 = 64
LSTM_CELLS_2 = 128
DENSE_UNITS_1 = 64
DENSE_UNITS_2 = 32

class sentiment_analysis_lstm(Model):
	def __init__(self):
		super(sentiment_analysis_lstm, self).__init__()
		self.embedding_1 = Embedding(VOCAB_SIZE,EMBEDDING_DIM)
		self.lstm_1 = Bidirectional(LSTM(LSTM_CELLS_1, return_sequences=True))
		self.lstm_2 = Bidirectional(LSTM(LSTM_CELLS_2))
		self.normalization = BatchNormalization()
		self.dense_1 = Dense(DENSE_UNITS_1, activation='relu')
		self.dense_2 = Dense(DENSE_UNITS_2, activation='relu')
		self.dense_3 = Dense(LABEL_SIZE, activation='softmax')
	def call(self,x):
		print(x.shape)
		#print(x.get_shape())
		x = self.embedding_1(x)
		x = self.lstm_1(x)
		x = self.lstm_2(x)
		x = self.normalization(x)
		x = self.dense_1(x)
		x = self.dense_2(x)
		x = self.dense_3(x)
		return x



model = sentiment_analysis_lstm()



loss_object = tf.keras.losses.CategoricalCrossentropy()
optimizer = tf.keras.optimizers.RMSprop(learning_rate=0.000001)

train_loss = tf.keras.metrics.Mean(name='train_loss')
train_accuracy = tf.keras.metrics.CategoricalAccuracy(name='train_accuracy')

test_loss = tf.keras.metrics.Mean(name='test_loss')
test_accuracy = tf.keras.metrics.CategoricalAccuracy(name='test_accuracy')



@tf.function
def train_step(sentences, labels):
	with tf.GradientTape() as tape:
		predictions = model(sentences)
		loss = loss_object(labels, predictions)
		gradients = tape.gradient(loss, model.trainable_variables)
		optimizer.apply_gradients(zip(gradients, model.trainable_variables))

	train_loss(loss)
	train_accuracy(labels, predictions)


@tf.function
def test_step(images, labels):
	predictions = model(images)
	t_loss = loss_object(labels, predictions)

	test_loss(t_loss)
	test_accuracy(labels, predictions)




for epoch in range(EPOCHS):
	for inputs,labels in train_ds:
		train_step(inputs,labels)

	for test_inputs,test_labels in test_ds:
		test_step(test_inputs,test_labels)

	template = 'Epoch: {}, Loss: {}, Acc: {}, Test Loss: {}, Test Acc: {}'

	print(template.format(
		epoch+1,train_loss.result(),train_accuracy.result()*100,test_loss.result(),
		test_accuracy.result()*100)
	)

model.save_weights(SAVE_PATH,save_format='tf')













