# import the necessary packages
import argparse
import cv2
import numpy as np


def get_point_from_mouse(event, x, y, flags, param):
    # if the left mouse button was clicked, record the (x, y) coordinates and draw the location on the image
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x, y))
        cv2.circle(image, center=(x, y), radius=5, color=(0, 255, 0), thickness=-1)


def long_axis_resize(image, new_size):
    # resize the image
    height, width = image.shape[1], image.shape[0]
    if height > width:
        new_height = new_size
        resize_ratio = new_height / height
        new_width = int(resize_ratio * width)
    else:
        new_width = new_size
        resize_ratio = new_width / width
        new_height = int(resize_ratio * height)

    return cv2.resize(image, (new_height, new_width)), resize_ratio


def get_4_points(image_path):

    # create references for global variables
    global refPt, image

    # initialize the list of reference points
    refPt = []

    viewing_size = 800

    # load the image, resize and clone it
    image = cv2.imread(image_path)
    image, resize_ratio = long_axis_resize(image, viewing_size)
    clone = image.copy()

    # setup the mouse callback function
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", get_point_from_mouse)

    # keep looping until we collected 4 points or the 'c' key is pressed
    while len(refPt) < 4:

        # display the image and wait for a keypress
        cv2.imshow("image", image)

        key = cv2.waitKey(1) & 0xFF
        # if the 'r' key is pressed, reset the clicking region
        if key == ord("r"):
            image = clone.copy()
        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            break

    # # display the final chosen points
    # cv2.imshow("image", image)
    # cv2.waitKey(0)

    # close all open windows
    cv2.destroyAllWindows()

    refPt = np.asarray(refPt) / resize_ratio

    return refPt.astype(int)


if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="Path to the image")
    args = vars(ap.parse_args())
    get_4_points(args["image"])
