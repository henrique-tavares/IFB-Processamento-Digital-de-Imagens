import cv2
from os import path

image_in = cv2.imread(path.join(path.curdir, "baboon.png"), 1)
image_out = cv2.imread(path.join(path.curdir, "baboon_out.png"), 1)
cv2.imshow("baboon_in", image_in)
cv2.imshow("baboon_out", image_out)
cv2.waitKey(0)
cv2.destroyAllWindows()
