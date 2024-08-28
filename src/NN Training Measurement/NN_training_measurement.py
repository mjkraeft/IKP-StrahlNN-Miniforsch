import numpy as np
import matplotlib.pyplot as plt
import math

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
#import tensorflow as tf
import keras

import keras_tuner

from scipy.stats import gaussian_kde


amount_outputs = 4


input_file_path = 'preprocess_input.txt'
output_file_path = 'preprocess_output.txt'

model_file_path = 'model.keras'


def getLabeledData(training_frac: float, validation_frac: float, test_frac: float):

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

    #if amount_outputs == 4:
    #    y = np.delete(y,[4,5],1)


    if x.shape[0] != y.shape[0]:
        raise ValueError('Number of samples do not match. (x: ' + str(x.shape[0]) + ', y: ' + str(y.shape[0]) + ')')

    if test_frac + training_frac + validation_frac > 1.:
        raise ValueError('Fractions do not sum to one')

    amount_samples = x.shape[0]
    training_index = int(math.floor(training_frac * amount_samples))
    validation_index = int(math.floor(validation_frac * amount_samples))
    testing_index = int(math.floor(test_frac * amount_samples))

    x_training_set = x[:training_index]
    y_training_set = y[:training_index]

    x_validation_set = x[1+training_index : training_index+validation_index]
    y_validation_set = y[1+training_index : training_index+validation_index]

    x_test_set = x[-testing_index:-1]
    y_test_set = y[-testing_index:-1]

    print(x_training_set.shape)
    print(y_training_set.shape)

    print(x_validation_set.shape)
    print(y_validation_set.shape)

    print(x_test_set.shape)
    print(y_test_set.shape)

    return (x_training_set, y_training_set), (x_validation_set, y_validation_set), (x_test_set, y_test_set)


def train_model(training_set: tuple[np.ndarray, np.ndarray], validation_set: tuple[np.ndarray, np.ndarray],):




    lossFunktion = keras.losses.Huber(
        delta=0.1,
        #reduction="sum_over_batch_size",
        name="huber_loss"
    )

    #lossFunktion = tf.keras.losses.MeanAbsoluteError()


    #activationFunktion = lambda a: tf.keras.activations.leaky_relu(a, negative_slope=0.2)


    model = keras.models.Sequential([
        keras.Input(shape=(7,)),
        keras.layers.Dense(400,
                              activation= 'relu',
                              use_bias=True),
        keras.layers.Dropout(0.01),
        #tf.keras.layers.BatchNormalization(),
        keras.layers.Dense(400,
                              activation= 'relu',
                              use_bias=True),
        keras.layers.Dropout(0.01),
        #tf.keras.layers.BatchNormalization(),
        keras.layers.Dense(100,
                              activation= 'relu',
                              use_bias=True),
        #tf.keras.layers.Dropout(0.001),
        # tf.keras.layers.BatchNormalization(),
        keras.layers.Dense(amount_outputs, use_bias=True)
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
    history = model.fit(training_set[0], training_set[1],
              epochs=12,
              validation_data=validation_set,
              #shuffle=True,
              )

    return model, history



def train_optimized_model(model, x: np.array, y: np.array):


    history = model.fit(x, y,
                        epochs=12,
                        validation_split=0.3,
                        shuffle=True,
                        )

    return model, history


def build_model(hp):
    #activation = hp.Choice("activation", ["relu", "tanh"])
    activation = "relu"
    #units = hp.Int("units", min_value = 10, max_value = 400, step = 5)
    num_layers = hp.Int('num_layers',min_value = 1, max_value = 5, step = 1)
    #biased = hp.Boolean('biased')
    biased = True
    dropout_rate = hp.Float('dropout_rate',min_value = 0., max_value = 0.3, step = 0.005)

    model = keras.Sequential()
    model.add(keras.Input(shape=(7,)))

    for i in range(num_layers):
        model.add(keras.layers.Dense(
                                    units=hp.Int('units_' + str(i), min_value=10, max_value=400, step=5),
                                    #units=units,
                                     activation=activation,
                                     use_bias=biased,
                                     ))
        model.add(keras.layers.Dropout(dropout_rate))

    model.add(keras.layers.Dense(amount_outputs, use_bias=biased))


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

    """
    tuner = keras_tuner.RandomSearch(
        hypermodel=build_model,
        objective="val_loss",
        max_trials=20,
        executions_per_trial=1,
        overwrite=True,
        directory="tuner",
        project_name="tuner_project",
    )
    """

    tuner = keras_tuner.BayesianOptimization(
    hypermodel=build_model,
    objective="val_loss",
    max_trials=20,
    executions_per_trial=1,
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
                 validation_split=0.3,
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



    training_set, validation_set, test_set = getLabeledData(0.7, 0.25,0.05)




    #print()

    model,history = train_model(training_set, validation_set)

    #model = hyperparam_optimisation(x,y)
    #model, history = train_optimized_model(model,x,y)

    #saveModel(model)

    model = loadModel()


    test_set_pre = model.predict(test_set[0])

    for i in range(test_set[1].shape[1]):
        plt.figure(dpi=200)
        xy = np.vstack([test_set_pre[:, i], test_set[1][:, i]])
        z = gaussian_kde(xy)(xy)

        plt.scatter(test_set[1][:,i], test_set_pre[:, i],
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


        labels = []
        if amount_outputs == 9:
            labels = ['x_pos', 'x_sig', 'x_amp', 'x_off', 'y_pos', 'y_sig', 'y_amp', 'y_off', 'x_int']
        elif amount_outputs == 4:
            labels = ['x_loc','x_sig','y_loc','y_sig']

        #plt.xlabel([
        #    'x_loc',
        #    'x_sig',
        #    'y_loc',
        #    'y_sig',
        #           ][i])

        plt.xlabel(labels[i])

        #plt.ylabel([
        #               'x_loc_pre',
        #               'x_sig_pre',
        #               'y_loc_pre',
        #               'y_sig_pre',
        #           ][i])

        plt.ylabel(labels[i] + '_pre')



        #plt.savefig([
        # 'x_loc_pre.png',
        # 'x_sig_pre.png',
        # 'y_loc_pre.png',
        # 'y_sig_pre.png',
        #][i])

        plt.savefig(labels[i] + '_pre.png')

        plt.show()

        









