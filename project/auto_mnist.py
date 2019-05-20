import sys
from keras.datasets import mnist
from keras.layers import Input, Dense
from keras.models import Model
import random
import numpy as np
import pandas as pd
import .pyplot as plt
import tkinter as tk
from PIL import Image
from PIL import ImageTk as tki

FEATURES = int(sys.argv[1])
EPOCHS = int(sys.argv[2])

input_img= Input(shape=(784,))

(X_train, _), (X_test, _) = mnist.load_data()

X_train = X_train.astype('float32')/255
X_test = X_test.astype('float32')/255

X_train = X_train.reshape(len(X_train), np.prod(X_train.shape[1:]))
X_test = X_test.reshape(len(X_test), np.prod(X_test.shape[1:]))

print(X_train.shape)
print(X_test[0])
encoded = Dense(units=128, activation='relu')(input_img)
encoded = Dense(units=64, activation='relu')(encoded)
encoded = Dense(units=FEATURES, activation='relu')(encoded)
decoded = Dense(units=64, activation='relu')(encoded)
decoded = Dense(units=128, activation='relu')(decoded)
decoded = Dense(units=784, activation='sigmoid')(decoded)

autoencoder=Model(input_img, decoded)

encoder = Model(input_img, encoded)

autoencoder.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])



autoencoder.fit(X_train, X_train,
                epochs=EPOCHS,
                batch_size=256,
                shuffle=True,
                validation_data=(X_test, X_test))

encoded_imgs = encoder.predict(X_test)
predicted = autoencoder.predict(X_test)

# plt.figure(figsize=(40, 4))
# for i in range(10):
#     # display original images
#     ax = plt.subplot(3, 20, i + 1)
#     plt.imshow(X_test[i].reshape(28, 28))
#     plt.gray()
#     ax.get_xaxis().set_visible(False)
#     ax.get_yaxis().set_visible(False)
    
#     # display encoded images
#     ax = plt.subplot(3, 20, i + 1 + 20)
#     plt.imshow(encoded_imgs[i].reshape(8,4))
#     plt.gray()
#     ax.get_xaxis().set_visible(False)
#     ax.get_yaxis().set_visible(False)

# # display reconstructed images
#     ax = plt.subplot(3, 20, 2*20 +i+ 1)
#     plt.imshow(predicted[i].reshape(28, 28))
#     plt.gray()
#     ax.get_xaxis().set_visible(False)
#     ax.get_yaxis().set_visible(False)
  
data = []
for l in autoencoder.layers:
    data.append(l.get_weights())
    # try:
    #     data += "Wieghts 1: " + str(len(l.get_weights()[0])) + "Weights 2: " + str(len(l.get_weights()[1])) + "\n"
    # except:
    #     data += "0" + "\n"
    #print(l.get_weights())
#print(data)
autoencoder.summary()
print(data == autoencoder.get_weights())
invector = Input(shape=(FEATURES,))
generator = Dense(units=64, activation='relu')(invector)
generator = Dense(units=128, activation='relu')(generator)
generator = Dense(units=784, activation='sigmoid')(generator)
gen_model = Model(invector, generator)

gen_model.summary()

for i in range(len(gen_model.layers) - 1):
    idx = -1 - i
    gen_model.layers[idx].set_weights(autoencoder.layers[idx].get_weights())
gen_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

sliders = []
def render(sliders, gui, lbl):
    to_predict = np.ndarray((1,FEATURES))
    
    for i in range(FEATURES):
        #rint(sliders[i].get())
        to_predict[0][i]=sliders[i].get()
    #print(to_predict)
    bip = gen_model.predict(to_predict)
    bip *= 255
    img = Image.fromarray(bip.reshape(28,28))
    img = img.resize((280,280), Image.ANTIALIAS)
    gui.disp_image = tki.PhotoImage(img)
    lbl.configure(image=gui.disp_image)
    # plt.figure(figsize=(20, 4))
    # plt.imshow(bip.reshape(28, 28))
    # plt.gray()
    # plt.show()

    gui.after(50, render, sliders, gui, lbl)

def load_val(sliders, encoder, X_test, gui, ex):
    vals = encoder.predict(X_test)
    to_load_i = random.randint(0, len(vals))
    to_load = vals[to_load_i]
    orig = X_test[to_load_i] * 255.0
    print(to_load)
    for i in range(len(to_load)):
        sliders[i].set(to_load[i])
    gui.ex_image = tki.PhotoImage(Image.fromarray(orig.reshape(28,28)).resize((280,280), Image.ANTIALIAS))
    
    ex.configure(image=gui.ex_image)
g = tk.Tk()

for i in range(FEATURES):
    
    sliders.append(tk.Scale(g, from_=0, to=30, resolution=.00000001))
    sliders[i].grid(column=i % 8, row=i // 8)
g.disp_image = tki.PhotoImage(Image.fromarray(np.ndarray((1,28*28)).reshape(28,28)))
l = tk.Label(g, image=g.disp_image)
l.grid(row= 5, column=5)
g.ex_image = tki.PhotoImage(Image.fromarray(np.ndarray((1,28*28)).reshape(28,28)))
l2 = tk.Label(g, image=g.ex_image)
l2.grid(row= 5, column=4)
tk.Button(g, text="Load Image", command=lambda: load_val(sliders, encoder, X_test, g, l2)).grid(row=5,column=1)
g.after(50, render, sliders, g, l)

g.mainloop()