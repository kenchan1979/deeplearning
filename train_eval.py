from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
import keras
import numpy as np
import tensorflow
import matplotlib.pyplot as plt

classes = ["Japanese_castle","Europe_castle","Chinese_castle"]
num_classes = len(classes)
image_size = 50

def main():
    X_train, X_test, y_train, y_test = np.load("./castle.npy",allow_pickle=True)
    X_train = X_train.astype("float") / 256
    X_test = X_test.astype("float") / 256
    y_train = np_utils.to_categorical(y_train, num_classes)
    y_test = np_utils.to_categorical(y_test, num_classes)

    model = model_train(X_train, y_train,X_test,y_test)
    model_eval(model, X_test, y_test)

def model_train(X, y, X_test,y_test):
    model = Sequential()
    model.add(Conv2D(32,(3,3), padding='same',input_shape=X.shape[1:]))
    model.add(Activation('relu'))
    model.add(Conv2D(32,(3,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64,(3,3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64,(3,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(3))
    model.add(Activation('softmax'))

    opt = tensorflow.keras.optimizers.RMSprop(lr=0.0001, decay=1e-6)
    model.compile(loss='categorical_crossentropy',optimizer=opt,metrics=['accuracy'])
    history=model.fit(X, y, batch_size=32, epochs=20,validation_data=(X_test, y_test))

    acc=history.history['accuracy']
    val_acc=history.history['val_accuracy']
    epochs=len(acc)
    
    plt.plot(range(epochs), acc, marker = '.', label = 'accuracy')
    plt.plot(range(epochs), val_acc, marker = '.', label = 'val_accuracy')
    plt.legend(loc = 'best')
    plt.grid()
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.show()

    model.save('./castle_cnn.h5')

    return model

def model_eval(model, X, y):
    scores = model.evaluate(X, y, verbose=1)
    print('Test Loss: ', scores[0])
    print('Test Accuracy: ', scores[1])

if __name__ == "__main__":
    main()