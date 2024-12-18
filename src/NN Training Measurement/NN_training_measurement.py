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


def getLabeledDataOld():
    '''
    Reads training Data from input_file_path and output_file_path
    Warning deprecated
    :return: training data x,y
    '''

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


def getLabeledData(training_frac: float, validation_frac: float, test_frac: float):
    '''
    Reads training Data from input_file_path and output_file_path
    TODO: make validation set constant set; i.e. count from back
    TODO: factor function with Shap Analysis.py
    :param training_frac:
    :param validation_frac:
    :param test_frac:
    :return: training data split into training set, validation set, test_set
    '''


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

    if amount_outputs == 4:
        y = np.delete(y,[4,5],1)


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


    return (x_training_set, y_training_set), (x_validation_set, y_validation_set), (x_test_set, y_test_set)



def train_model(training_set: tuple[np.ndarray, np.ndarray], validation_set: tuple[np.ndarray, np.ndarray]):
    '''
    Trains a new model on training set.
    :param training_set:
    :param validation_set:
    :return: model and training history
    '''


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
        keras.layers.Dropout(0.02),
        #tf.keras.layers.BatchNormalization(),
        keras.layers.Dense(400,
                              activation= 'relu',
                              use_bias=True),
        keras.layers.Dropout(0.02),
        #tf.keras.layers.BatchNormalization(),
        keras.layers.Dense(10,
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
                      'mean_absolute_error',
                      'mean_squared_error',

                  ]
                  )

    # train the model
    history = model.fit(training_set[0], training_set[1],
              epochs=30,
              validation_data=validation_set,
              shuffle=True,
              )

    return model, history



def train_optimized_model(model: keras.models.Sequential, training_set: tuple[np.ndarray, np.ndarray], validation_set: tuple[np.ndarray, np.ndarray]):
    '''
    Trains an existing model on training set.
    :param training_set:
    :param validation_set:
    :return: model and training history
    '''

    history = model.fit(training_set[0], training_set[1],
                        epochs=60,
                        validation_data=validation_set,
                        shuffle=True,
                        batch_size=100,
                        )

    return model, history


class HyperModel(keras_tuner.HyperModel):
    '''
    Extension of keras_tuner.HyperModel for hyperparameter tuning.
    Tunable hp are (at time of writing):
        - num_layers
        (- biased *NO PERFORMANCE IMPROVEMENT FOUND BY BIASED = FALSE)
        - dropout_rate
        - num_units_per_layer
        - batch_size (while fitting)

    Using Huber loss, Adam optimizer
    '''


    def build(self, hp):
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
                          'mean_absolute_error',
                          'mean_squared_error',

                      ]
                      )

        return model

    def fit(self, hp, model, *args, **kwargs):
        return model.fit(
            *args,
            batch_size = hp.Int("batch_size", min_value=50, max_value=200, step=10),
            **kwargs,
        )


def hyperparam_optimisation(training_set: tuple[np.ndarray, np.ndarray], validation_set: tuple[np.ndarray, np.ndarray]):
    '''
    New hyperparameter optimization for training data
    :param training_set:
    :param validation_set:
    :return: best model
    '''


    hp = keras_tuner.HyperParameters()
    hypermodel = HyperModel()



    #build_model(keras_tuner.HyperParameters())

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
    hypermodel=hypermodel,
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

    tuner.search(training_set[0], training_set[1],
                 epochs=10,
                 validation_data=validation_set,
                 shuffle=True,
                 #batch_size = 100,
                 )

    models = tuner.get_best_models(num_models=1)
    best_model = models[0]
    best_model.summary()

    return best_model


def training_set_size_optimisation():
    '''
    Tests best achievable performance for an interval of training data sizes.
    By commenting in/out below switch between training single modle or full hyperparameter tuning for each traing set size.
    :return:
    '''
    training_set_fracs = np.arange(0.01,0.6,0.01)
    results = np.zeros((training_set_fracs.shape[0], 3), dtype=float)


    for i,t_s in enumerate(training_set_fracs):

        print()
        print()
        print("Testing training_set_frac: " + str(t_s) + "\t(%i/%i)" % (i+1, training_set_fracs.shape[0]))

        validation_frac = 0.25
        test_frac = 0.05
        training_set, validation_set, test_set = getLabeledData(t_s, validation_frac, test_frac)

        model, history = train_model(training_set, validation_set)

        #model = hyperparam_optimisation(training_set, validation_set)
        #model, history = train_optimized_model(model, training_set, validation_set)

        results[i] = model.evaluate(test_set[0], test_set[1])


    np.savetxt('training_set_size_opti/training_set_size_opti.txt',np.append(training_set_fracs.reshape(training_set_fracs.shape[0],-1), results, axis=1))

    for i in range(results.shape[1]):
        plt.figure(dpi = 200)

        plt.plot(training_set_fracs, results[:,i],
                 linewidth = 0.5
                 )

        plt.xlabel('training_frac')

        plt.ylabel(['test_loss',
                  'mean_absolute_error',
                  'mean_squared_error',
                  ][i])

        plt.grid()

        plt.savefig('training_set_size_opti/' +
            ['test_loss',
                  'mean_absolute_error',
                  'mean_squared_error',
                  ][i] + '.png')

        plt.show()




def saveModel(model: keras.models.Sequential):
    '''
    Saves model
    :param model:
    :return:
    '''
    model.save(model_file_path)


def loadModel():
    '''
    Loads model
    :return:
    '''
    return keras.models.load_model(model_file_path)

def visualize_training_set_size_optimisation():

    '''
    For training set size optimisation: graphs performance over training set size.
    :return:
    '''

    simple_model_training_set_opti_results = np.loadtxt('training_set_size_opti_1/training_set_size_opti.txt')
    hyper_model_training_set_opti_results = np.loadtxt('training_set_size_opti/training_set_size_opti.txt')



    for i in range(1,simple_model_training_set_opti_results.shape[1]):
        plt.figure(dpi=800)

        plt.plot(simple_model_training_set_opti_results[:, 0], simple_model_training_set_opti_results[:, i], label = "simple")
        plt.plot(hyper_model_training_set_opti_results[:, 0], hyper_model_training_set_opti_results[:, i], label = "hyper")

        plt.xlabel('training_frac')

        plt.ylabel(['test_loss',
                    'mean_absolute_error',
                    'mean_squared_error',
                    ][i-1])

        plt.legend()

        plt.grid()



        plt.savefig('training_set_size_opti_1/compare/' +['test_loss',
                  'mean_absolute_error',
                  'mean_squared_error',
                  ][i-1] + '.png')

        plt.show()


def visualize_model_testing(model: keras.models.Sequential, test_set):
    '''
    Visualizes model performance with identify graphs. (i.e. predicted data over measured data with pretty density on z axis)
    :param model:
    :param test_set:
    :return:
    '''
    test_set_pre = model.predict(test_set[0])
    for i in range(test_set[1].shape[1]):
        plt.figure(dpi=200)
        xy = np.vstack([test_set_pre[:, i], test_set[1][:, i]])
        z = gaussian_kde(xy)(xy)

        plt.scatter(test_set[1][:, i], test_set_pre[:, i],
                    c=z,
                    marker='.',
                    s=1,
                    )

        x1 = -2.1
        y1 = -2.1
        x2 = 2.1
        y2 = 2.1

        plt.plot([x1, x2], [y1, y2],
                 color='red',
                 linewidth='1',
                 linestyle='dotted',
                 )

        plt.xlim(x1, x2)
        plt.ylim(y1, y2)

        labels = []
        if amount_outputs == 9:
            labels = ['x_pos', 'x_sig', 'x_amp', 'x_off', 'y_pos', 'y_sig', 'y_amp', 'y_off', 'x_int']
        elif amount_outputs == 4:
            labels = ['x_loc', 'x_sig', 'y_loc', 'y_sig']

        # plt.xlabel([
        #    'x_loc',
        #    'x_sig',
        #    'y_loc',
        #    'y_sig',
        #           ][i])

        plt.xlabel(labels[i])

        # plt.ylabel([
        #               'x_loc_pre',
        #               'x_sig_pre',
        #               'y_loc_pre',
        #               'y_sig_pre',
        #           ][i])

        plt.ylabel(labels[i] + '_pre')

        # plt.savefig([
        # 'x_loc_pre.png',
        # 'x_sig_pre.png',
        # 'y_loc_pre.png',
        # 'y_sig_pre.png',
        # ][i])

        plt.title(f"Training: {training_frac}, Validation: {validation_frac}, Testing: {test_frac}")

        plt.savefig(labels[i] + '_pre.png')

        plt.show()




if __name__ == '__main__':



    training_frac = 0.1
    validation_frac = 0.25
    test_frac = 0.5
    #training_set, validation_set, test_set = getLabeledData(training_frac, validation_frac, test_frac)



    #print()

    #model,history = train_model(training_set, validation_set)

    #model = hyperparam_optimisation(training_set, validation_set)
    #model, history = train_optimized_model(model,training_set, validation_set)

    #saveModel(model)

    #model = loadModel()

    #evaluation_result = model.evaluate(test_set[0], test_set[1])
    #print(evaluation_result)

    #visualize_model_testing(model)

    #training_set_size_optimisation()

    visualize_training_set_size_optimisation()

        









