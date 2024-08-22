import numpy as np
import math
import matplotlib.pyplot as plt


mouse_click_file_path = 'mouse_click_event.txt'
input_file_path = 'input.txt'
input_element_file_path = 'input_element_list.txt'
prepro_input_file_path = 'preprocess_input.txt'

input_data_range_min = -1.
input_data_range_max = 1.


def calculateScale():




    pixel_points = np.loadtxt(mouse_click_file_path,
                              delimiter=' ',
                              skiprows=1)


    pixel_dis = math.sqrt((pixel_points[0][0]-pixel_points[1][0])**2 + (pixel_points[0][1]-pixel_points[1][1])**2)
    proper_dis = 20.     # mm

    scale = proper_dis/pixel_dis



    offset = (
        int(pixel_points[2][0]),
        int(pixel_points[2][1])
    )

    return scale, offset




def preprocessInputData():

    input_data = np.loadtxt(input_file_path,
                            delimiter=' ',
                            unpack=True
                            )

    data_range = [max(abs(min(d)), abs(max(d))) for d in input_data]
    data_ranges = np.swapaxes(np.array([[-1 * s for s in data_range], data_range]), 0, 1)

    input_data = np.array([np.interp(d, data_ranges[i], [input_data_range_min, input_data_range_max]) for i, d in enumerate(input_data)])
    input_data = np.array([input_data[:,i] for i in range(input_data.shape[1])])

    np.savetxt(prepro_input_file_path, input_data)



def preprocessOutputData(scale: float, offset: (int, int)):
    print()



if __name__ == '__main__':
    #print(calculateScale())

    preprocessInputData()