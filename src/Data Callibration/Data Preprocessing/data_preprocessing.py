import numpy as np
import math
import matplotlib.pyplot as plt


mouse_click_file_path = 'mouse_click_event.txt'


input_file_path = 'input.txt'
input_element_file_path = 'input_element_list.txt'
prepro_input_file_path = 'preprocess_input.txt'


output_file_path = 'output.txt'
output_element_file_path = 'outputs_list.txt'
prepro_output_file_path = 'preprocess_output.txt'

input_data_range_min = -1.
input_data_range_max = 1.

output_data_range_min = -1.
output_data_range_max = 1.


def calculateScale():

    pixel_points = np.loadtxt(mouse_click_file_path,
                              delimiter=' ',
                              skiprows=1)


    pixel_dis_1 = math.sqrt((pixel_points[0][0]-pixel_points[4][0])**2 + (pixel_points[0][1]-pixel_points[4][1])**2)
    pixel_dis_2 = math.sqrt((pixel_points[3][0]-pixel_points[5][0])**2 + (pixel_points[3][1]-pixel_points[5][1])**2)
    pixel_dis = (pixel_dis_1 + pixel_dis_2) * 0.5

    proper_dis = 20.     # mm

    scale = proper_dis/pixel_dis



    center1 = (
        (pixel_points[0][0] + pixel_points[1][0]) * 0.5,
        (pixel_points[0][1] + pixel_points[1][1]) * 0.5,
    )

    center2 = (
        (pixel_points[2][0] + pixel_points[3][0]) * 0.5,
        (pixel_points[2][1] + pixel_points[3][1]) * 0.5,
    )



    center = (
        int(np.round((np.mean([center1[0], center2[0]])))),
        int(np.round((np.mean([center1[1], center2[1]])))),
            )


    return scale, center




def preprocessInputData():

    input_data = np.loadtxt(input_file_path,
                            delimiter=' ',
                            unpack=True
                            )


    output_data = np.loadtxt(output_file_path,
                             delimiter=' ',
                             )

    out_of_bounds_data_points = [i for i in range(output_data.shape[0]) if output_data[i, -1] == 0.]
    input_data = np.delete(input_data, out_of_bounds_data_points, axis=1)


    data_range = [max(abs(min(d)), abs(max(d))) for d in input_data]
    data_ranges = np.swapaxes(np.array([[-1 * s for s in data_range], data_range]), 0, 1)

    input_data = np.array([np.interp(d, data_ranges[i], [input_data_range_min, input_data_range_max]) for i, d in enumerate(input_data)])
    input_data = np.array([input_data[:,i] for i in range(input_data.shape[1])])

    np.savetxt(prepro_input_file_path, input_data)



def preprocessOutputData(scale: float, offset: (int, int)):
    output_data = np.loadtxt(output_file_path,
                              delimiter=' ',
                              )

    out_of_bounds_data_points = [i for i in range(output_data.shape[0]) if output_data[i, -1] == 0.]
    output_data = np.delete(output_data, out_of_bounds_data_points, axis=0)

    data_ranges = [max(abs(min(output_data[:, i])), abs(max(output_data[:, i]))) for i in range(output_data.shape[1])]


    output_data = np.array([
        output_data[:, i]
        for i in range(output_data.shape[1])
    ])

    output_data = np.array([np.interp(d, [-1 * data_ranges[i], data_ranges[i]], [output_data_range_min, output_data_range_max]) for i, d in enumerate(output_data)])

    output_data = np.array([
        output_data[:, i]
        for i in range(output_data.shape[1])
    ])


    output_data = np.append(output_data[:,1:3],output_data[:,5:7], axis=1)



    np.savetxt(prepro_output_file_path, output_data)



if __name__ == '__main__':
    scale, center = calculateScale()

    preprocessInputData()
    preprocessOutputData(scale, center)
