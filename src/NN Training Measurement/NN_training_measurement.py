import numpy as np
import matplotlib.pyplot as plt
import math

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
#import tensorflow as tf
import keras

import keras_tuner

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



    lossFunktion = keras.losses.Huber(
        delta=0.1,
        #reduction="sum_over_batch_size",
        name="huber_loss"
    )

    #lossFunktion = tf.keras.losses.MeanAbsoluteError()


    #activationFunktion = lambda a: tf.keras.activations.leaky_relu(a, negative_slope=0.2)


    model = keras.models.Sequential([
        keras.Input(shape=(7,)),
        keras.layers.Dense(100,
                              activation= 'relu',
                              use_bias=True),
        keras.layers.Dropout(0.01),
        #tf.keras.layers.BatchNormalization(),
        keras.layers.Dense(100,
                              activation= 'relu',
                              use_bias=True),
        keras.layers.Dropout(0.01),
        #tf.keras.layers.BatchNormalization(),
        keras.layers.Dense(10,
                              activation= 'relu',
                              use_bias=True),
        #tf.keras.layers.Dropout(0.001),
        # tf.keras.layers.BatchNormalization(),
        keras.layers.Dense(4, use_bias=True)
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
    history = model.fit(x, y,
              epochs=25,
              validation_split = 0.1,
              shuffle=True,
              )

    return model, history



def train_optimized_model(model, x: np.array, y: np.array):


    history = model.fit(x, y,
                        epochs=25,
                        validation_split=0.1,
                        shuffle=True,
                        )

    return model, history


def build_model(hp):
    #activation = hp.Choice("activation", ["relu", "tanh"])
    activation = "relu"
    #units = hp.Int("units", min_value = 10, max_value = 400, step = 5)
    num_layers = hp.Int('num_layers',min_value = 1, max_value = 10, step = 1)
    #biased = hp.Boolean('biased')
    biased = True

    model = keras.Sequential()
    model.add(keras.Input(shape=(7,)))

    for i in range(num_layers):
        model.add(keras.layers.Dense(
                                    units=hp.Int('units_' + str(i), min_value=10, max_value=400, step=5),
                                    #units=units,
                                     activation=activation,
                                     use_bias=biased,
                                     ))
        model.add(keras.layers.Dropout(0.01))

    model.add(keras.layers.Dense(4, use_bias=biased))


    lossFunktion = keras.losses.Huber(
        delta=0.1,
        # reduction="sum_over_batch_size",
        name="huber_loss"
    )


    model.compile(optimizer='adam',
                  loss=lossFunktion,
                  metrics=[
                      # 'mean_squared_error',
                      'mean_absolute_error',
                  ]
                  )

    return model


def hyperparam_optimisation(x: np.array, y: np.array):

    build_model(keras_tuner.HyperParameters())

    tuner = keras_tuner.RandomSearch(
        hypermodel=build_model,
        objective="val_loss",
        max_trials=10,
        executions_per_trial=2,
        overwrite=True,
        directory="tuner",
        project_name="tuner_project",
    )

    tuner = keras_tuner.BayesianOptimization(
    hypermodel=build_model,
    objective="val_loss",
    max_trials=10,
    executions_per_trial=2,
    #num_initial_points=None,
    #alpha=0.0001,
    #beta=2.6,
    #seed=None,
    #hyperparameters=None,
    #tune_new_entries=True,
    #allow_new_entries=True,
    #max_retries_per_trial=0,
    #max_consecutive_failed_trials=3,
    overwrite=True,
    directory="tuner",
    project_name="tuner_project",
    )

    tuner.search(x, y,
                 epochs=10,
                 validation_split=0.1,
                 shuffle=True,
                 )

    models = tuner.get_best_models(num_models=1)
    best_model = models[0]
    best_model.summary()

    return best_model


def saveModel(model: keras.models.Sequential):
    model.save(model_file_path)


def loadModel():
    return keras.models.load_model(model_file_path)

if __name__ == '__main__':



    x, y = getLabeledData()




    #model,history = train_model(x,y)

    model = hyperparam_optimisation(x,y)
    model, history = train_optimized_model(model,x,y)

    saveModel(model)

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

        x1 = -2.1
        y1 = -2.1
        x2 = 2.1
        y2 = 2.1

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

        









