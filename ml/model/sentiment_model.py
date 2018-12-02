import tensorflow as tf
import keras
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Conv1D
from keras.layers import MaxPooling1D
from keras.callbacks import ModelCheckpoint
from keras.callbacks import TensorBoard
from keras.utils import to_categorical

lstm_size = 256
lstm_layers = 2
batch_size = 100
embedded_size = 300
learning_rate = .001
n_words = 56675
epochs = 100
dropout = 0.2
X = np.load("../Data/content.npy")
Y = np.load("../Data/sentiment.npy")
print(Y.shape)

unique = set(Y)
dictionary = {}
for i, word in enumerate(unique):
	dictionary.update({word: i})
for i, cat in enumerate(Y):
	Y[i] = dictionary.get(cat)
train_X = X[:35000]
train_X = np.resize(train_X, (len(train_X), 1, 150))
val_X = X[-5000:]
val_X = np.resize(val_X, (len(val_X), 1, 150))
train_Y = Y[:35000]
train_Y = to_categorical(train_Y)
val_Y = Y[-5000:]
val_Y = to_categorical(val_Y)
print(train_X.shape, val_X.shape)
print(train_Y.shape, val_Y.shape)

model = Sequential()

model.add(LSTM(lstm_size, return_sequences=True, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dropout(dropout))
model.add(Conv1D(filters=32, kernel_size=2, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(LSTM(lstm_size))
model.add(Dropout(dropout))
# model.add(LSTM(lstm_size))
# model.add(Dropout(dropout))
model.add(Dense(train_Y.shape[1], activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy', optimizer='adam')

tensorboard = TensorBoard(log_dir="logs/{}", histogram_freq=0, batch_size=batch_size, write_graph=False,
                          write_grads=False, write_images=False, embeddings_freq=0, embeddings_layer_names=None,
                          embeddings_metadata=None)

filepath = "checkpoints/best.hdf5"

checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=False, mode='min')
model.fit(train_X, train_Y, epochs=epochs, batch_size=batch_size, callbacks=[checkpoint, tensorboard])
