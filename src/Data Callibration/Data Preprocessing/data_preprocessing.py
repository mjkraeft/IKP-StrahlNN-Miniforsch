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

input_data_range_min = 0.
input_data_range_max = 1.

output_data_range_min = 0.
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



ptsToRemove = [2228,
               15161,
               ]

#ptsToRemove = []

def preprocessData(scale_type = 'normalize'):


    input_data = np.loadtxt(input_file_path,
                            delimiter=' ',
                            unpack=True
                            )

    output_data = np.loadtxt(output_file_path,
                             delimiter=' ',
                             )

    input_data = np.delete(input_data, ptsToRemove, 1)
    output_data = np.delete(output_data, ptsToRemove, axis=0)

    out_of_bounds_data_points = [i for i in range(output_data.shape[0]) if output_data[i, -1] == 0.]
    input_data = np.delete(input_data, out_of_bounds_data_points, axis=1)
    output_data = np.delete(output_data, out_of_bounds_data_points, axis=0)




    if scale_type == 'normalize':



        #input_data = (input_data - input_data.mean(axis=1)) / input_data.std(axis=1)
        #output_data = (output_data - np.mean(output_data, axis=0)) / np.std(output_data, axis=0)

        output_data = np.array([
            output_data[:, i]
            for i in range(output_data.shape[1])
        ])



        scaling_factor_intput = 2
        scaling_factor_output = 2
        input_data = np.array([(d - d.mean() * scaling_factor_intput) / d.std() for d in input_data])
        output_data = np.array([(d - d.mean()) / (d.std() * scaling_factor_output) for d in output_data])  #TODO: normalization deal with division by std = 0 errors

        output_data = np.array([
            output_data[:, i]
            for i in range(output_data.shape[1])
        ])

        input_data = np.array([input_data[:, i] for i in range(input_data.shape[1])])


        output_data = np.append(output_data[:, 1:3], output_data[:, 5:7], axis=1)

        for i in range(input_data.shape[1]):
            plt.hist(input_data[:, i], bins=50, color='blue')
            plt.show()

        plt.hist(output_data[:, 0], bins=50, color='red')
        plt.show()

    elif scale_type == 'min_max':

        data_range_input = [max(abs(min(d)), abs(max(d))) for d in input_data]
        data_ranges_input = np.swapaxes(np.array([[-1 * s for s in data_range_input], data_range_input]), 0, 1)

        input_data = np.array([np.interp(d, data_ranges_input[i], [input_data_range_min, input_data_range_max]) for i, d in enumerate(input_data)])
        input_data = np.array([input_data[:, i] for i in range(input_data.shape[1])])



        data_ranges_output = [(min(output_data[:, i]), max(output_data[:, i])) for i in range(output_data.shape[1])]

        output_data = np.array([
            output_data[:, i]
            for i in range(output_data.shape[1])
        ])

        output_data = np.array(
            [np.interp(d, [data_ranges_output[i][0], data_ranges_output[i]][1], [output_data_range_min, output_data_range_max]) for i, d
             in enumerate(output_data)])

        output_data = np.array([
            output_data[:, i]
            for i in range(output_data.shape[1])
        ])

        output_data = np.append(output_data[:, 1:3], output_data[:, 5:7], axis=1)




    np.savetxt(prepro_output_file_path, output_data)
    np.savetxt(prepro_input_file_path, input_data)


def preprocessInputData():

    input_data = np.loadtxt(input_file_path,
                            delimiter=' ',
                            unpack=True
                            )

    input_data = np.delete(input_data, ptsToRemove, 1)

    output_data = np.loadtxt(output_file_path,
                             delimiter=' ',
                             )
    output_data = np.delete(output_data, ptsToRemove, axis=0)

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
    output_data = np.delete(output_data, ptsToRemove, axis=0)

    out_of_bounds_data_points = [i for i in range(output_data.shape[0]) if output_data[i, -1] == 0.]
    output_data = np.delete(output_data, out_of_bounds_data_points, axis=0)


    data_ranges = [(min(output_data[:, i]), max(output_data[:, i])) for i in range(output_data.shape[1])]

    print(data_ranges)

    output_data = np.array([
        output_data[:, i]
        for i in range(output_data.shape[1])
    ])

    output_data = np.array([np.interp(d, [data_ranges[i][0], data_ranges[i]][1], [output_data_range_min, output_data_range_max]) for i, d in enumerate(output_data)])

    output_data = np.array([
        output_data[:, i]
        for i in range(output_data.shape[1])
    ])


    output_data = np.append(output_data[:,1:3],output_data[:,5:7], axis=1)



    np.savetxt(prepro_output_file_path, output_data)



if __name__ == '__main__':
    scale, center = calculateScale()

    #preprocessInputData()
    #preprocessOutputData(scale, center)

    preprocessData(scale_type='normalize')
