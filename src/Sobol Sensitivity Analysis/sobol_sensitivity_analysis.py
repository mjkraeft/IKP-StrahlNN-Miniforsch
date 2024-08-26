import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from SALib.sample import saltelli
from SALib.analyze import sobol


model_file_path = 'model.keras'
numOutPuts = 4

def loadModel():
    return tf.keras.models.load_model(model_file_path)


def printStackedBar(Si):


    #print([str(0)].extend(Si[0]['S1']))

    data = []
    for i in range(numOutPuts):
        a = [
            [
                'x_loc',
                'x_sig',
                'y_loc',
                'y_sig',
            ][i]
        ]
        a.extend(Si[i]['ST'])
        data.append(a)

    columns = ['Input']
    columns.extend([ 'I0SH02',
                        'I0SV02',
                        'I0SH03',
                        'I0SV03',
                        'I0LE01',
                        'I0QU01',
                        'I0QU03',
                        ])


    df = pd.DataFrame(
        data,
        columns=columns
    )

    print(df)

    plt.figure(dpi = 400)
    df.plot(x='Input', kind='bar', stacked=True,
            title='Sensitivity')

    plt.ylim(bottom=0)
    plt.savefig('sensitivity.png')
    plt.show()






if __name__ == '__main__':


    model = loadModel()

    problem =  {
            'num_vars' : 7,
            'names' : [ 'I0SH02',
                        'I0SV02',
                        'I0SH03',
                        'I0SV03',
                        'I0LE01',
                        'I0QU01',
                        'I0QU03',
                        ],
            'bounds' : [
                [0.,1.]
                for i in range(7)
            ]
        }



    param_values = saltelli.sample(problem, 2**16)


    y = model.predict(param_values)

    Si = []

    for i in range(numOutPuts):
        Si.append(sobol.analyze(problem,y[:,i],
                                parallel=True,
                                n_processors = 16,
                                print_to_console=True,
        ))

        print()

    #for i in range(numOutPuts):
    #    print(str(i) + ' : ' + str(Si[i]['S1']))


    printStackedBar(Si)


