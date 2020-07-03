# import the necessary packages
import numpy as np
import cv2


def order_points(pts):
    # initialize a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    pts = np.asarray(pts).astype(int)
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


def get_four_point_transform_matrix(image, pts, dst):
    # obtain a consistent order of the points and unpack them individually
    rect = order_points(pts)
    # (tl, tr, br, bl) = rect
    dst = order_points(dst)

    # # compute the width of the new image, which will be the
    # # maximum distance between bottom-right and bottom-left
    # # x-coordinates or the top-right and top-left x-coordinates
    # widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    # widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    # maxWidth = max(int(widthA), int(widthB))
    #
    # # compute the height of the new image, which will be the
    # # maximum distance between the top-right and bottom-right
    # # y-coordinates or the top-left and bottom-left y-coordinates
    # heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    # heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    # maxHeight = max(int(heightA), int(heightB))

    # # construct the set of destination points to obtain a "birds eye view" of the image, again specifying points
    # # in the top-left, top-right, bottom-right, and bottom-left order
    # dst = np.array([
    #     [0, 0],
    #     [maxWidth - 1, 0],
    #     [maxWidth - 1, maxHeight - 1],
    #     [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    transform_matrix = cv2.getPerspectiveTransform(rect, dst)

    # warped = cv2.warpPerspective(image, transform_matrix, (maxWidth, maxHeight))

    return transform_matrix


def get_transformed_coordinates(transform_matrix, coors_list):
    new_coors_list = []
    for coors in coors_list:
        np_coors = np.array(coors)
        np.append(np_coors, 1)
        new_coors = (np.dot(transform_matrix[0, :], np_coors), np.dot(transform_matrix[1, :], np_coors))
        new_coors /= np.dot(transform_matrix[2, :], np_coors)
        new_coors_list.append(new_coors)

    return new_coors_list
