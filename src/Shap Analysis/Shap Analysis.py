import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
import shap


model_file_path = 'model.keras'
numOutPuts = 4

def loadModel():
    return tf.keras.models.load_model(model_file_path)


input_param_list = ['I0SH02',
           'I0SV02',
           'I0SH03',
           'I0SV03',
           'I0LE01',
           'I0QU01',
           'I0QU03',
           ]

output_param_list = [
            'x_loc',
            'x_sig',
            'y_loc',
            'y_sig',
        ]

input_file_path = 'preprocess_input.txt'
output_file_path = 'preprocess_output.txt'

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

    if numOutPuts == 4:
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


if __name__ == '__main__':
    model = loadModel()

    training_frac = 0.6
    validation_frac = 0.2
    test_frac = 0.15
    training_set, validation_set, test_set = getLabeledData(training_frac, validation_frac, test_frac)

    explainer = shap.Explainer(model.predict, test_set[0])
    shap_values = explainer(test_set[0])

    shap.plots.beeswarm(shap_values)


