import numpy as np

from matplotlib import pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, Dropout, Conv2D,MaxPooling2D,BatchNormalization
from tensorflow.keras.callbacks import ModelCheckpoint
from data import validation_generator, train_generator
from tensorflow.keras.regularizers import l2, l1, l1_l2


num_train = 28709
num_val = 7178
num_epoch = 50

def plot_model_history(model_history):

    fig, axs = plt.subplots(1,2,figsize=(15,5))
    # summarize history for accuracy
    axs[0].plot(range(1,len(model_history.history['accuracy'])+1),model_history.history['accuracy'])
    axs[0].plot(range(1,len(model_history.history['val_accuracy'])+1),model_history.history['val_accuracy'])
    axs[0].set_title('Model Accuracy')
    axs[0].set_ylabel('Accuracy')
    axs[0].set_xlabel('Epoch')
    axs[0].set_xticks(np.arange(1,len(model_history.history['accuracy'])+1),len(model_history.history['accuracy'])/10)
    axs[0].legend(['train', 'val'], loc='best')
    # summarize history for loss
    axs[1].plot(range(1,len(model_history.history['loss'])+1),model_history.history['loss'])
    axs[1].plot(range(1,len(model_history.history['val_loss'])+1),model_history.history['val_loss'])
    axs[1].set_title('Model Loss')
    axs[1].set_ylabel('Loss')
    axs[1].set_xlabel('Epoch')
    axs[1].set_xticks(np.arange(1,len(model_history.history['loss'])+1),len(model_history.history['loss'])/10)
    axs[1].legend(['train', 'val'], loc='best')
    fig.savefig('plot.png')
    plt.show()


model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), padding='same', input_shape=(48,48,1)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Conv2D(64, kernel_size=(3, 3), padding='same', bias_regularizer=l1_l2(l1=0.01, l2=0.01)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
model.add(Dropout(0.5))

model.add(Conv2D(128, kernel_size=(3, 3), padding='same', bias_regularizer=l1_l2(l1=0.01, l2=0.01)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
model.add(Dropout(0.5))

model.add(Conv2D(128, kernel_size=(3, 3), padding='same', bias_regularizer=l1_l2(l1=0.01, l2=0.01)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(1024, activation='relu', bias_regularizer=l1_l2(l1=0.01, l2=0.01)))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax', bias_regularizer=l1_l2(l1=0.01, l2=0.01)))

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
checkpoint = ModelCheckpoint(filepath='checkpoints/model-{epoch:03d}.hdf5', save_weights_only=True, monitor='val_accuracy',save_best_only=True,mode='auto')
model_info = model.fit_generator(
        train_generator,
        epochs=num_epoch,
        validation_data=validation_generator,
        callbacks=[checkpoint])

plot_model_history(model_info)