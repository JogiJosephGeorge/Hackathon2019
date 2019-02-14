from keras.backend.tensorflow_backend import flatten
print ("Start")

import numpy
import pandas
import matplotlib.pyplot as plt
import math

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Flatten
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from numpy import array

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
   

import pandas
import matplotlib.pyplot as plt
dataset = pandas.read_csv('DataToTeach.csv',engine='python')
plt.plot(dataset)
plt.show()

# fix random seed for reproducibility
numpy.random.seed(7)

dataframe = pandas.read_csv('DataToTeach.csv', engine='python')
dataset = array(dataframe.values)
dataset = dataset.astype('float32')

def get_train():
    lstmInput = []
    for i in range(len(dataset)):
        row = [dataset[i][0], [dataset[i][1], dataset[i][2], dataset[i][3], dataset[i][4]], dataset[i][5]]
        lstmInput.append(row)
    return lstmInput

# define model
model = Sequential()
model.add(LSTM(10, input_shape=(1,1)))
model.add(Dense(1, activation='linear'))
# compile model
model.compile(loss='mse', optimizer='adam')
# fit model
dataframe = get_train()
model.fit(dataframe, epochs=300, shuffle=False, verbose=0)
# save model to single file
model.save('lstm_model.h5')

print ("End")
