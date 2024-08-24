import numpy as np
import matplotlib.pyplot as plt
import math

import tensorflow as tf

from scipy.stats import gaussian_kde



input_file_path = 'preprocess_input.txt'
output_file_path = 'preprocess_output.txt'

model_file_path = 'model.keras'

def getLabeledData ():

    x = np.loadtxt(input_file_path,
                   delimiter=' ',
                   #max_rows=10
                   )

    #x = [np.array(x[:,i]) for i in range(x.shape[1])]

    y = np.loadtxt(output_file_path,
                   delimiter=' ',
                   #max_rows=10
                   )

    #y = [np.array(y[:,i]) for i in range(y.shape[1])]

    return x, y


def train_model(x: np.array, y: np.array):



    lossFunktion = tf.keras.losses.Huber(
        delta=0.3,
        #reduction="sum_over_batch_size",
        name="huber_loss"
    )

    #lossFunktion = tf.keras.losses.MeanAbsoluteError()


    #activationFunktion = lambda a: tf.keras.activations.leaky_relu(a, negative_slope=0.2)


    model = tf.keras.models.Sequential([
        tf.keras.Input(shape=(7,)),
        tf.keras.layers.Dense(400,
                              activation= 'relu',
                              use_bias=True),
        tf.keras.layers.Dropout(0.01),
        #tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(400,
                              activation= 'relu',
                              use_bias=True),
        tf.keras.layers.Dropout(0.01),
        #tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(100,
                              activation= 'relu',
                              use_bias=True),
        #tf.keras.layers.Dropout(0.001),
        # tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(4, use_bias=True)
    ])
    # compile the model
    model.compile(optimizer='adam',
                  loss=lossFunktion,
                  metrics=[
                      #'mean_squared_error',
                      'mean_absolute_error',
                  ]
                  )
    # train the model
    model.fit(x, y, epochs=25)

    return model


def saveModel(model: tf.keras.models.Sequential):
    model.save(model_file_path)


def loadModel():
    return tf.keras.models.load_model(model_file_path)

if __name__ == '__main__':

    x, y = getLabeledData()




    #model = train_model(x,y)
    #saveModel(model)

    model = loadModel()


    y_predict = model.predict(x)

    for i in range(y.shape[1]):
        plt.figure(dpi=200)
        xy = np.vstack([y_predict[:,i], y[:,i]])
        z = gaussian_kde(xy)(xy)

        plt.scatter(y[:,i],y_predict[:,i],
                    c=z,
                    marker = '.',
                    s=1,
                    )

        x1 = -0.1
        y1 = -0.1
        x2 = 1.1
        y2 = 1.1

        plt.plot([x1,x2], [y1,y2],
                 color = 'red',
                 linewidth='1',
                 linestyle='dotted',
                 )

        plt.xlim(x1,x2)
        plt.ylim(y1,y2)

        plt.xlabel([
            'x_loc',
            'x_sig',
            'y_loc',
            'y_sig',
                   ][i])

        plt.ylabel([
                       'x_loc_pre',
                       'x_sig_pre',
                       'y_loc_pre',
                       'y_sig_pre',
                   ][i])

        plt.savefig([
         'x_loc_pre.png',
         'x_sig_pre.png',
         'y_loc_pre.png',
         'y_sig_pre.png',
        ][i])
        plt.show()
        









