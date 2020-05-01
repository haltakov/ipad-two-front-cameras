import numpy as np

#    4   5   6   7
#   10   0   0  40
# start = 5
# end = 7
# length = 2
# color_change = 30
# color_step = 10


def fill_hole(row, start, end):
    """
    Fills a signle whole in an image row
    """
    if start == 0:
        return

    length = end-start

    start_color = row[start-1].astype(np.float)
    color_change = row[end].astype(np.float) - start_color
    color_step = color_change / (length+1)

    for i in range(0, length):
        row[start + i] = start_color + color_step*(i+1)


def fill_holes(image):
    """
    Fill all holes in an image
    """
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


def compute_virtual_camera_image(image_left, image_right, disp_left, disp_right, offset):
    """
    Computer an image from a virtual camera
    """

    virtual_image = np.zeros(image_left.shape, image_left.dtype)

    project_image(image_left, virtual_image, disp_left * offset, left_to_right=True)
    project_image(image_right, virtual_image, disp_right * (1-offset), left_to_right=False)

    fill_holes(virtual_image)

    return virtual_image


def project_image(image, target_image, disparity, left_to_right=True):
    """
    Project an image to the target image using the disparity
    """

    direction = -1 if left_to_right else 1

    for y in range(0, len(image)):
        row = image[y]

        for i in range(0, len(row)):
            if left_to_right:
                x = i
            else:
                x = len(row) - 1 - i

            target_x = int(round(x + direction*disparity[y][x]))
            if 0 <= target_x < len(row):
                target_image[y][target_x] = row[x]
