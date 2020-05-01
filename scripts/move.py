import numpy as np
import cv2


def fill_hole(row, start, end):
    if start == 0:
        return

    length = end-start

    start_color = row[start-1]
    color_offset = row[end] - start_color

    for i in range(0, length):
        row[i+start] = start_color + color_offset * i/length


def fill_holes(image):
    for i in range(0, len(image)):
        row = image[i]

        hole_j = -1
        for j in range(0, len(row)):
            if np.count_nonzero(row[j]) == 0:
                if hole_j == -1:
                    hole_j = j
            elif hole_j > -1:
                fill_hole(row, hole_j, j)
                hole_j = -1



left = cv2.imread('../images/left2.png', cv2.IMREAD_UNCHANGED)
right = cv2.imread('../images/right2.png', cv2.IMREAD_UNCHANGED)
disp = cv2.imread('../images/disp.png', cv2.IMREAD_UNCHANGED)
disp_rev = cv2.flip(cv2.imread('../images/disp_mir.png', cv2.IMREAD_UNCHANGED), 1)

cv2.imshow('disp', disp)
fill_holes(disp)
cv2.imshow('disp fh', disp)

fill_holes(disp_rev)


d = disp / 256
d2 = d / 2

d_rev = disp_rev / 256
d2_rev = d_rev / 2




center = np.zeros(left.shape, left.dtype)

for i in range(0, len(left)):
    row = left[i]
    for j in range(0, len(row)):
        new_j = int(round(j - d2[i][j]))
        if new_j >= 0:
            center[i][new_j] = row[j]

for i in range(0, len(right)):
    row = right[i]
    for jj in range(0, len(row)):
        j = 480-1-jj
        new_j = int(round(j + d2_rev[i][j]))
        if new_j < 480:
            center[i][new_j] = row[j]

cv2.imshow('center', center)
fill_holes(center)
cv2.imshow('center_fh', center)

# cv2.imshow('image', left)

# cv2.imshow('disp', disp_rev)
# cv2.imshow('right', right)

cv2.imwrite('../images/center2.png', center)

# 241, 233 --> 100

cv2.waitKey(0)
cv2.destroyAllWindows()