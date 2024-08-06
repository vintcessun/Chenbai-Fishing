import os
import glob
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers, optimizers, losses, regularizers, Sequential
from keras.callbacks import EarlyStopping, Callback
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model

tags={"pre":"还没有执行钓鱼操作",
      "begin":"执行了钓鱼操作但是没有鱼上来",
      "find":"有鱼了",
      "none":"黑块",
      "normal":"白块",
      "perfect":"黄块",
      "wait":"打完了一次等待一下",
      "finished":"钓鱼完成",
      "score":"钓鱼完成获得计分板"}

number_tag={0:"none",
1:"normal",
2:"perfect"
}

def read_img(path):
    cate = [path + x for x in os.listdir(path) if os.path.isdir(path + x)]
    imgs = []
    labels = []
    for idx, folder in enumerate(cate):
        for im in glob.glob(folder + '/*.png'):
            img = cv2.imread(im)
            img = img.reshape(256,256,3)
            imgs.append(img)
            labels.append(idx)
            
    return np.asarray(imgs, np.float32), np.asarray(labels, np.int32)
 

data, label = read_img('data\\')

def trans(label):
    ret = []
    for i in label:
        if(i==0):
            ret.append([1,0,0])
        elif i==1:
            ret.append([0,1,0])
        elif i==2:
            ret.append([0,0,1])
    return np.asarray(ret,np.int32)

ratio = 0.8

num_example = data.shape[0]
arr = np.arange(num_example)
np.random.shuffle(arr)
data = data[arr]
label = label[arr]
data = data /255.0
label = trans(label)
s = np.int_(num_example * ratio)
x_train = data[:s]
y_train = label[:s]
x_val = data[s:]
y_val = label[s:]

class MyEarlyStopping(keras.callbacks.Callback):
    def __init__(self, patience=0):
        super(MyEarlyStopping, self).__init__()
        self.patience = patience
        self.best_weights = None

    def on_train_begin(self, logs=None):
        self.wait = 0
        self.stopped_epoch = 0
        self.best = 0.0

    def on_epoch_end(self, epoch, logs=None):
        current = logs.get("accuracy")*ratio+logs.get("val_accuracy")*(1-ratio)
        print(f"\nTotal accuracy: {current}")
        if np.greater(current, self.best):
            self.best = current
            self.wait = 0
            self.best_weights = self.model.get_weights()
        else:
            self.wait += 1
            if self.wait >= self.patience:
                self.stopped_epoch = epoch
                self.model.stop_training = True
                print("Restoring model weights from the end of the best epoch.")
                self.model.set_weights(self.best_weights)

    def on_train_end(self, logs=None):
        if self.stopped_epoch > 0:
            print("Epoch %05d: early stopping" % (self.stopped_epoch + 1))


model = Sequential()

model.add(layers.Conv2D(32, (3,3), padding='same', input_shape=(256, 256, 3)))
model.add(layers.BatchNormalization())
model.add(layers.Activation('elu'))
model.add(layers.Conv2D(32, (3,3), padding='same'))
model.add(layers.BatchNormalization())
model.add(layers.Activation('elu'))
model.add(layers.MaxPooling2D(pool_size=(2,2)))
model.add(layers.Dropout(0.2))

model.add(layers.Conv2D(64, (3,3), padding='same')) 
model.add(layers.BatchNormalization())
model.add(layers.Activation('elu'))
model.add(layers.Conv2D(64, (3,3), padding='same'))
model.add(layers.BatchNormalization())
model.add(layers.Activation('elu'))
model.add(layers.MaxPooling2D(pool_size=(2,2)))
model.add(layers.Dropout(0.2))

model.add(layers.Conv2D(128, (3,3), padding='same'))
model.add(layers.BatchNormalization())
model.add(layers.Activation('elu'))
model.add(layers.Conv2D(128, (3,3), padding='same'))
model.add(layers.BatchNormalization())
model.add(layers.Activation('elu'))
model.add(layers.MaxPooling2D(pool_size=(2,2)))
model.add(layers.Dropout(0.3))

model.add(layers.Flatten())
model.add(layers.Dense(64, activation=None))
model.add(layers.BatchNormalization())
model.add(layers.Activation('elu'))
model.add(layers.Dropout(0.3))
model.add(layers.Dense(3, activation='softmax'))

model.summary()

#early_stop = EarlyStopping(monitor='val_accuracy', mode='max', patience=3, verbose=1, restore_best_weights=True)
early_stop = MyEarlyStopping(patience=5)

model.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.Nadam(learning_rate=0.0025), metrics=['accuracy'])

datagen = ImageDataGenerator()

flow_train = datagen.flow(x_train, y_train, batch_size=32)
flow_val = datagen.flow(x_val, y_val, batch_size=32)
flow_test = datagen.flow(data, label, batch_size=32)

model.fit(flow_train ,steps_per_epoch=x_train.shape[0]/32, epochs=200, validation_data=flow_val, callbacks=[early_stop])
score = model.evaluate(flow_test, verbose=0)
#print('Test loss:', score[0])
print('Test accuracy:', score[1])
load_model = load_model("model")
load_score = load_model.evaluate(flow_test, verbose=0)
print('load accuracy:', load_score[1])
if load_score[1]<score[1]:
    print("better")
    model.save("model")
os.system("start restart.bat")