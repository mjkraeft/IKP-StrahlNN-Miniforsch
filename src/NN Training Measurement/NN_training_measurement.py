import numpy as np
import matplotlib.pyplot as plt
import math

import tensorflow as tf



input_file_path = 'preprocess_input.txt'
output_file_path = 'preprocess_output.txt'

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



if __name__ == '__main__':

    x, y = getLabeledData()


    model = tf.keras.models.Sequential([
        tf.keras.Input(shape = (7,)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(4)
    ])

    # compile the model
    model.compile(optimizer='adam',
                  loss='mse',
                  metrics=['accuracy']
                  )
    # train the model
    model.fit(x, y, epochs=100)




