import cv2

mouse_click_file_path = 'mouse_click_event.txt'
image_file_path = 'I0T5 vor einbau.png'

window_size = (1400,800)


def mouse_click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        with open(mouse_click_file_path, 'a') as f:
            f.write('\n')
            f.write(str(x) + ',' + str(y))



if __name__ == '__main__':

    with open(mouse_click_file_path, 'w') as f:
        f.write('x-location,y-location')

    img = cv2.imread(image_file_path, 1)



    width_scale = window_size[0] / img.shape[1]
    height_scale = window_size[1] / img.shape[0]

    scale = min(width_scale, height_scale)
    width_window = int(img.shape[1] * scale)
    height_window = int(img.shape[0] * scale)

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', width_window, height_window)

    cv2.setMouseCallback('image', mouse_click_event)

    cv2.imshow('image', img)

    cv2.waitKey(0)

    cv2.destroyAllWindows()


