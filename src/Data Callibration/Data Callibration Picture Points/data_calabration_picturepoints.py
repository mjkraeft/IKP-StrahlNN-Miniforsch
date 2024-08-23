"""
This python File open an image in a separate window. Clicking on a pixel with left click
then saves that pixels coordinates in a txt file.The window can be closed by pressing '0'.
"""

import cv2
import numpy as np
import math

mouse_click_file_path = 'mouse_click_event.txt'         # file path where selected pixel coords are to be saved
image_file_path = 'I0T5 vor einbau.png'                 # file path of image to be opened

window_size = (1600, 1600)                               # target pixel size of window to be opened


def calculateScale():

    pixel_points = np.loadtxt(mouse_click_file_path,
                              delimiter=' ',
                              skiprows=1)


    pixel_dis_1 = math.sqrt((pixel_points[0][0]-pixel_points[4][0])**2 + (pixel_points[0][1]-pixel_points[4][1])**2)
    pixel_dis_2 = math.sqrt((pixel_points[3][0]-pixel_points[5][0])**2 + (pixel_points[3][1]-pixel_points[5][1])**2)
    pixel_dis = (pixel_dis_1 + pixel_dis_2) * 0.5

    proper_dis = 20.     # mm

    scale = proper_dis/pixel_dis

    print((pixel_dis, pixel_dis_1, pixel_dis_2))


    center1 = (
        (pixel_points[0][0] + pixel_points[1][0]) * 0.5,
        (pixel_points[0][1] + pixel_points[1][1]) * 0.5,
    )

    center2 = (
        (pixel_points[2][0] + pixel_points[3][0]) * 0.5,
        (pixel_points[2][1] + pixel_points[3][1]) * 0.5,
    )

    #print(center1, center2)


    center = (
        int(np.round((np.mean([center1[0], center2[0]])))),
        int(np.round((np.mean([center1[1], center2[1]])))),
            )


    return scale, center

def mouse_click_event(event, x, y, flags, param):
    """
    Function that is called when a mouse button is pressed.
    If left mouse button is pressed,
    save the pixels coordinates of click in a txt file.
    If right mouse button is pressed, generates a new, empty file.
    """
    if event == cv2.EVENT_LBUTTONDOWN:
        with open(mouse_click_file_path, 'a') as f:
            f.write('\n')
            f.write(str(x) + ' ' + str(y))
    elif event == cv2.EVENT_RBUTTONDOWN:
        with open(mouse_click_file_path, 'w') as f:
           f.write('x_pos y_pos')


def show_scale_center(img: np.ndarray):
    image_scale, center = calculateScale()

    centerDotSize = 1
    for i in range((-1 * centerDotSize), centerDotSize + 1):
        for j in range((-1 * centerDotSize), centerDotSize + 1):
            img[center[1] + i, center[0] + j] = [0, 0, 255]
    line_width = 2
    line_length_mm = 10
    line_start = (492, 619)
    for i in range(int(line_length_mm // image_scale)):
        for j in range(line_width):
            img[line_start[1] + j, line_start[0] + i] = [0, 0, 0]


if __name__ == '__main__':

    # writes file header and deletes contents of file of 'mouse_click_file_path' if it already existed
    #with open(mouse_click_file_path, 'w') as f:
    #    f.write('x_pos y_pos')


    # open image with openCV
    img = cv2.imread(image_file_path, 1)


    # calculate window size to match aspect ratio of image. The resulting window will be at
    # most as big as the target size.
    width_scale = window_size[0] / img.shape[1]
    height_scale = window_size[1] / img.shape[0]

    scale = min(width_scale, height_scale)
    width_window = int(img.shape[1] * scale)
    height_window = int(img.shape[0] * scale)

    # opening (and closing) window with OpenCV
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', width_window, height_window)

    cv2.setMouseCallback('image', mouse_click_event)

    show_scale_center(img)

    cv2.imshow('image', img)

    print("Data Calibration: Centering excepts clicks top left, bottom right, top right, bottom left.")
    print("Data Calibration: Scale excepts two clicks on left side 10mm lines.")

    cv2.waitKey(0)

    cv2.destroyAllWindows()
