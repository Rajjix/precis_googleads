import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.layers.normalization import BatchNormalization


def train_model(train_data_path: str):

    dataset = np.genfromtxt(train_data_path, delimiter=',')
    # skip first row.
    # columns to predict are (0, 1)
    # columns to train from are (2, 3, 4, 5, 6, 7)
    X = dataset[1:, 2:]
    y = dataset[1:, :2]

    model = Sequential()
    model.add(Dense(64, input_dim=6, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dense(2, activation='softplus'))
    model.compile(loss='mse',
                  optimizer='adam', metrics=['mae', 'mse'])

    model.fit(X, y, epochs=150, batch_size=25)

    # save stuff related to our model creation/prediction in one dir.
    train_dir = '/'.join(train_data_path.split('/')[:-1])
    model.save(f'{train_dir}/google_ads_model.h5')
