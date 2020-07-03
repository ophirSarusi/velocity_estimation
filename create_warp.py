# import the necessary packages
from transform_utils import get_four_point_transform_matrix
from user_interface_utils import get_4_points
import argparse
import cv2


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to the image file")
ap.add_argument("-m", "--map", help="path to the map file")
args = vars(ap.parse_args())

# load the image and grab the source coordinates (i.e. the list of
# of (x, y) points)
image_path = args["image"]
map_path = args["map"]
image = cv2.imread(image_path)
pts = get_4_points(image_path)
dst = get_4_points(map_path)

# apply the four point transform to obtain a "birds eye view" of the image
transform_matrix = get_four_point_transform_matrix(image, pts, dst)
warped = cv2.warpPerspective(image, transform_matrix, (image.shape[1], image.shape[0]))

# show the original and warped images
cv2.imshow("Original", image)
cv2.imshow("Warped", warped)
cv2.waitKey(0)
