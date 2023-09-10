import  numpy as np
import matplotlib.pyplot as plt
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense,Conv2D,MaxPool2D,Flatten,Dropout
import tensorflow as tf
# get the data & preprocess it
(X_train, y_train), (X_test, y_test)=mnist.load_data()
X_train.shape,y_train.shape,X_test.shape,y_test.shape
def plot_input_image(i):
    plt.imshow(X_train[i],cmap='binary')
    plt.title(y_train[i])
    # plt.axes('off')
    plt.show()
for i in range(0):
    plot_input_image(i)

# pre process the image
# normalizing the image to [0,1] range
X_train=X_train.astype(np.float32)/255.0
X_test=X_test.astype(np.float32)/255.0

# reshape / expand the dimention of images to (28,28,1)
X_train=np.expand_dims(X_train,-1)
X_test=np.expand_dims(X_test,-1)
# convert classes to one hot value
y_train=keras.utils.to_categorical(y_train)
y_test=keras.utils.to_categorical(y_test)

model=Sequential()
model.add(Conv2D(32,(3,3),input_shape=(28,28,1),activation='relu'))
model.add(MaxPool2D((2,2)))
model.add(Conv2D(64,(3,3),activation='relu'))
model.add(MaxPool2D((2,2)))
model.add(Flatten())
model.add(Dropout(0.25))
model.add(Dense(10,activation='softmax'))
model.summary()
# compile model
model.compile(optimizer='adam', loss=keras.losses.categorical_crossentropy,metrics=['accuracy'])
# opt = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9)
# model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

# callbacks
from keras.callbacks import EarlyStopping,ModelCheckpoint
# EarlyStoping
es=EarlyStopping(monitor='val_acc',min_delta=0.01,patience=4,verbose=1)

# Model Check points
mc=ModelCheckpoint("./bestModel.h5",monitor='val_acc',verbose=1,save_best_only=True)

cb=[es,mc]

# calculating the training time
from timeit import default_timer
def trainModel():
    start=default_timer()
    # model training
    his=model.fit(X_train,y_train, epochs=5, validation_split=0.3, callbacks=cb)
    print("Total training time is : ",default_timer()-start)

trainModel()

model.save("bestModel.h5")
from keras.models import load_model
model_S=load_model("bestModel.h5")
score=model_S.evaluate(X_test,y_test)
print(f" the model accuracy is {score[1]}")