from dataclasses import dataclass

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D


@dataclass(repr=True, frozen=True)
class ModelConfig:
    BATCH_SIZE: int = 64
    NUM_CLASSES: int = 10
    EPOCHS: int = 30
    IMAGE_HEIGHT: int = 28
    IMAGE_WIDTH: int = 28


if __name__ == '__main__':
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train = x_train.reshape(x_train.shape[0], ModelConfig.IMAGE_HEIGHT, ModelConfig.IMAGE_WIDTH, 1)
    x_test = x_test.reshape(x_test.shape[0], ModelConfig.IMAGE_HEIGHT, ModelConfig.IMAGE_WIDTH, 1)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255

    y_train = keras.utils.to_categorical(y_train, 10)
    y_test = keras.utils.to_categorical(y_test, 10)

    model = Sequential()

    model.add(Conv2D(filters=32,
                     kernel_size=(3, 3),

                     activation='relu',
                     input_shape=x_train.shape[1:]))
    model.add(Conv2D(filters=32,
                     kernel_size=(3, 3),
                     activation='relu'))

    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(rate=0.25))
    model.add(Conv2D(filters=128,
                     kernel_size=(3, 3),
                     activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(rate=0.25))

    model.add(Flatten())
    model.add(Dense(units=128, activation='relu'))
    model.add(Dropout(rate=0.5))
    model.add(Dense(units=64, activation='relu'))
    model.add(Dropout(rate=0.5))
    model.add(Dense(units=ModelConfig.NUM_CLASSES, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adam(),
                  metrics=['accuracy'])
    model.fit(x_train, y_train,
              batch_size=ModelConfig.BATCH_SIZE,
              epochs=ModelConfig.EPOCHS,
              verbose=1,
              validation_data=(x_test, y_test))
    model.save('digit_recognition_model.keras')
