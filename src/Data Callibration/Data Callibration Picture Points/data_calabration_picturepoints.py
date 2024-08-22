"""
This python File open an image in a separate window. Clicking on a pixel with left click
then saves that pixels coordinates in a txt file.The window can be closed by pressing '0'.
"""

import cv2

mouse_click_file_path = 'mouse_click_event.txt'         # file path where selected pixel coords are to be saved
image_file_path = 'I0T5 vor einbau.png'                 # file path of image to be opened

window_size = (1400, 800)                               # target pixel size of window to be opened


def mouse_click_event(event, x, y, flags, param):
    """
    Function that is called when a mouse button is pressed. If left mouse button is pressed,
    save the pixels coordinates of click in a txt file.
    """
    if event == cv2.EVENT_LBUTTONDOWN:
        with open(mouse_click_file_path, 'a') as f:
            f.write('\n')
            f.write(str(x) + ' ' + str(y))


if __name__ == '__main__':

    # writes file header and deletes contents of file of 'mouse_click_file_path' if it already existed
    with open(mouse_click_file_path, 'w') as f:
        f.write('x_pos,y_pos')


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

    cv2.imshow('image', img)

    cv2.waitKey(0)

    cv2.destroyAllWindows()
