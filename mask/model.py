import numpy as np

from matplotlib import pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, Dropout, Conv2D,MaxPooling2D
from tensorflow.keras.callbacks import ModelCheckpoint
from data import validation_generator, train_generator



show_accuracy = 0
Show_loss = 0


model=Sequential()

model.add(Conv2D(200,(3,3),input_shape=(150, 150, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(100,(3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
model.add(Dropout(0.5))

model.add(Dense(50,activation='relu'))

model.add(Dense(2,activation='softmax'))


model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

checkpoint = ModelCheckpoint(filepath='checkpoints/model-{epoch:03d}.hdf5',monitor='val_loss',verbose=0,save_best_only=True,mode='auto')
history = model.fit_generator(train_generator,epochs=10,validation_data=validation_generator,callbacks=[checkpoint])


if(Show_loss):
    plt.plot(history.history['loss'],'r',label='training loss')
    plt.plot(history.history['val_loss'],label='validation loss')
    plt.xlabel('# epochs')
    plt.ylabel('loss')
    plt.legend()
    plt.show()


if(show_accuracy):
    plt.plot(history.history['accuracy'],'r',label='training accuracy')
    plt.plot(history.history['val_accuracy'],label='validation accuracy')
    plt.xlabel('# epochs')
    plt.ylabel('loss')
    plt.legend()
    plt.show()

print(model.evaluate(train_generator,validation_generator))