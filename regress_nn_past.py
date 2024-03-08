import pickle

import xarray

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Activation, Dropout
from tensorflow.keras.models import Model

x = xarray.open_dataarray('data/x_training_past.nc')
pcs = xarray.open_dataarray('data/pcs_training_past.nc')

sc = StandardScaler()

X_train = sc.fit_transform(x)
y_train = pcs

input_layer = Input(shape=(X_train.shape[1],))
dense_layer_1 = Dense(100, activation='relu')(input_layer)
dense_layer_2 = Dense(50, activation='relu')(dense_layer_1)
dense_layer_3 = Dense(25, activation='relu')(dense_layer_2)
output = Dense(2)(dense_layer_3)

model = Model(inputs=input_layer, outputs=output)
model.compile(loss="mean_squared_error", optimizer="adam", metrics=["mean_squared_error"])

history = model.fit(X_train, y_train, epochs=500, verbose=1)

pickle.dump(sc, open("data/scaler_past", "wb"))

model.save('data/nn_past')
