import numpy as np
import math
import matplotlib.pyplot as plt


mouse_click_file_path = 'mouse_click_event.txt'


input_file_path = 'input.txt'
input_element_file_path = 'input_element_list.txt'
prepro_input_file_path = 'preprocess_input.txt'
input_normalisations_file_path_1 = 'input_normalisations.txt_1'
input_normalisations_file_path_2 = 'input_normalisations.txt_2'


output_file_path = 'output.txt'
output_element_file_path = 'outputs_list.txt'
prepro_output_file_path = 'preprocess_output.txt'
output_normalisations_file_path_1 = 'output_normalisations_1.txt'
output_normalisations_file_path_2 = 'output_normalisations_2.txt'

input_data_range_min = 0.
input_data_range_max = 1.

output_data_range_min = 0.
output_data_range_max = 1.


scaling_factor_input = 2
scaling_factor_output = 2



#TODO: data_preprocessing figure out what each function does again for documentationgit



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



def scale_data_to_mm(data_file_path = '', data_save_path = ''):
    scale, center = calculateScale()
    center_used_offset = [116,312]

    print((scale, center))

    data = np.loadtxt(data_file_path, unpack=True)[0:4,:]

    data[0] = (data[0]-center[1]+center_used_offset[0])*scale
    data[2] = (data[2]-center[0]+center_used_offset[1])*scale

    data[1] = (data[1]) * scale
    data[3] = (data[3]) * scale

    data = np.array([data[:,i] for i in range(data.shape[1])])

    for i in range(data.shape[1]):
       plt.figure(dpi=300)
       plt.hist(data[:, i], bins=50, color='orange')
       plt.show()

    np.savetxt(data_save_path, data)



def calculate_intense(std, amp):
    if len(amp) != len(std):
        raise ValueError('Amplitude and std must be the same length')
    return amp * std * math.sqrt(2 * math.pi)


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




    x_intense = np.array(calculate_intense(output_data[:,2], output_data[:,3])).reshape((output_data.shape[0],-1))
    y_intense = np.array(calculate_intense(output_data[:,6], output_data[:,7])).reshape((output_data.shape[0],-1))

    keep_std_amount = 3 #TODO: make this dynamic, lim not hard coded

    x_intense_lim = (0.4e6, 2.25e6)
    y_intense_lim = (0.4e6, 2.25e6)

    intense_idx_remove = [i for i in range(output_data.shape[0]) if (
            x_intense[i] < x_intense_lim[0]
            or x_intense[i] > x_intense_lim[1]
            or y_intense[i] < y_intense_lim[0]
            or y_intense[i] > y_intense_lim[1]
    )]

    output_data = np.append(output_data, x_intense, axis=1)
    output_data = np.append(output_data, y_intense, axis=1)
    input_data = np.delete(input_data, intense_idx_remove, axis=1)
    output_data = np.delete(output_data, intense_idx_remove, axis=0)




    test = output_data.copy()  # TODO: remove

    test = np.array([test[:, i] for i in range(test.shape[1])])

    for i in range(test.shape[0]):
        if i not in [1, 2, 5, 6]:
            continue
        plt.figure(dpi=300)
        plt.hist(test[i, :], bins=50, color='blue')
        plt.show()




    input_data_norm_1 = []
    input_data_norm_2 = []
    output_data_norm_1 = []
    output_data_norm_2 = []

    if scale_type == 'normalize':



        #input_data = (input_data - input_data.mean(axis=1)) / input_data.std(axis=1)
        #output_data = (output_data - np.mean(output_data, axis=0)) / np.std(output_data, axis=0)

        output_data = np.array([
            output_data[:, i]
            for i in range(output_data.shape[1])
        ])





        input_data_norm_1 = [d.mean() for d in input_data]
        input_data_norm_2 = [d.std() for d in input_data]
        output_data_norm_1 = [d.mean() for d in output_data]
        output_data_norm_2 = [d.std() for d in output_data]

        input_data = np.array([(d - input_data_norm_1[i]) / (input_data_norm_2[i] * scaling_factor_input) if input_data_norm_2[i] != 0 else d for i,d in enumerate(input_data)])
        output_data = np.array([(d - output_data_norm_1[i]) / (output_data_norm_2[i] * scaling_factor_output) if output_data_norm_2[i] != 0 else d for i,d in enumerate(output_data)])

        output_data = np.array([
            output_data[:, i]
            for i in range(output_data.shape[1])
        ])

        input_data = np.array([input_data[:, i] for i in range(input_data.shape[1])])




        #for i in range(input_data.shape[1]):
        #    plt.figure(dpi = 300)
        #    plt.hist(input_data[:, i], bins=50, color='blue')
        #    plt.show()

        #for i in range(output_data.shape[1]):
        #    plt.figure(dpi=300)
        #    plt.hist(output_data[:, i], bins=50, color='red')
        #    plt.show()




    elif scale_type == 'min_max':

        raise NotImplementedError("min_max saving of scaling factor not implemented")

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

        #output_data = np.append(output_data[:, 1:3], output_data[:, 5:7], axis=1)


    #output_data = np.append(output_data[:, 1:3], output_data[:, 5:7], axis=1)
    output_data = np.append(np.append(output_data[:, 1:3], output_data[:, 5:7], axis=1), output_data[:,12:14], axis=1)
    output_data_norm_1 = np.append(np.append(output_data_norm_1[1:3], output_data_norm_1[5:7], axis=0), output_data_norm_1[12:14], axis=0)
    output_data_norm_2 = np.append(np.append(output_data_norm_2[1:3], output_data_norm_2[5:7], axis=0), output_data_norm_2[12:14], axis=0)


    #output_data = output_data[:, 1:10]

    np.savetxt(prepro_output_file_path, output_data)
    np.savetxt(prepro_input_file_path, input_data)

    np.savetxt(output_normalisations_file_path_1, output_data_norm_1)
    np.savetxt(output_normalisations_file_path_2, output_data_norm_2)

    np.savetxt(input_normalisations_file_path_1, input_data_norm_1)
    np.savetxt(input_normalisations_file_path_2, input_data_norm_2)









def deprocessData(data_path = '', data_norm_path_1 ='', data_norm_path_2 ='', data_save_path = '', scale_type ='normalize', data_type = ''):

    norms_1 = np.loadtxt(data_norm_path_1)
    norms_2 = np.loadtxt(data_norm_path_2)


    data = np.loadtxt(data_path, unpack=True)


    if scale_type == 'normalize':

        if data_type == 'input':
            scaling_factor = scaling_factor_input
        elif data_type == 'output':
            scaling_factor = scaling_factor_output
        else:
            raise ValueError("data_type must be 'input' or 'output'")


        data = np.array([(d * scaling_factor * norms_2[i]) + norms_1[i] if norms_2[i] != 0 else d for i,d in enumerate(data)])



    elif scale_type == 'min_max':
        raise NotImplementedError("min_max not implemented")

    else:
        raise NotImplementedError(str(scale_type) + " not implemented")

    data = np.array([data[:,i] for i in range(data.shape[1])])

    for i in range(data.shape[1]):
       plt.figure(dpi=300)
       plt.hist(data[:, i], bins=50, color='red')
       plt.show()

    np.savetxt(data_save_path, data)










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


def visualize_intense():
    intense = np.loadtxt(prepro_output_file_path,
               delimiter=' ',
               unpack=True,
               usecols=[4,5])

    x_intense_lim = (0.4e6,2.25e6)
    y_intense_lim = (0.4e6,2.25e6)

    intense_idx_remove = [i for i in range(intense.shape[1]) if (
        intense[0][i] < x_intense_lim[0]
        or intense[0][i] > x_intense_lim[1]
        or intense[1][i] < y_intense_lim[0]
        or intense[1][i] > y_intense_lim[1]
    )]

    #intense = np.delete(intense, intense_idx_remove, axis=1)

    #print(intense.shape)



    for d in intense:
        plt.figure(dpi = 400)



        plt.scatter(np.arange(0,len(d)),d,
                    marker='.',
                    s=1,

                    )

        m = np.mean(d)
        std = np.std(d)

        plt.plot([0,len(d)], [m,m],
                 color = 'red',
                 linewidth = 1.5,)

        plt.plot([0, len(d)], [m+std, m+std],
                 color='red',
                 linewidth=1.5,
                 linestyle='--')

        plt.plot([0, len(d)], [m - std, m - std],
                 color='red',
                 linewidth=1.5,
                 linestyle='--')

        plt.grid()

        plt.show()



if __name__ == '__main__':
    scale, center = calculateScale()

    #preprocessInputData()
    #preprocessOutputData(scale, center)

    preprocessData(scale_type='normalize')

    #testAmp = np.array([1.99, 0.55, 0.4])
    #testStd = np.array([0.2, 0.8, 1.])

    #print(calculate_intense(testStd, testAmp))

    #visualize_intense()

    deprocessData(data_path = 'preprocess_output.txt', data_norm_path_1 = output_normalisations_file_path_1, data_norm_path_2 = output_normalisations_file_path_2, data_save_path='deprocess_output.txt', scale_type='normalize', data_type='output')


    scale_data_to_mm(data_file_path='deprocess_output.txt', data_save_path='scale_output.txt')
