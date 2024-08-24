import numpy as np
import matplotlib.pyplot as plt
import math

import tensorflow as tf
import SALib


model_file_path = 'model.keras'

def loadModel():
    return tf.keras.models.load_model(model_file_path)