import pickle

import xarray

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Activation,Dropout
from tensorflow.keras.models import Model

x = xarray.open_dataarray('x_training_era.nc')
pcs = xarray.open_dataarray('pcs_training_era.nc')

#X_train, X_test, y_train, y_test = train_test_split(x, pcs, shuffle=False)

sc = StandardScaler()

X_train = sc.fit_transform(x)
y_train = pcs
#X_test = sc.transform(X_test)

input_layer = Input(shape=(X_train.shape[1],))
dense_layer_1 = Dense(100, activation='relu')(input_layer)
dense_layer_2 = Dense(50, activation='relu')(dense_layer_1)
dense_layer_3 = Dense(25, activation='relu')(dense_layer_2)
output = Dense(2)(dense_layer_3)

model = Model(inputs=input_layer, outputs=output)
model.compile(loss="mean_squared_error", optimizer="adam", metrics=["mean_squared_error"])

history = model.fit(X_train, y_train, epochs=200, verbose=1)

pickle.dump(sc, open("scaler_centered_era", "wb"))

model.save('nn_centered_era')

#print(model.evaluate(X_test, y_test))
