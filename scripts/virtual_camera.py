import numpy as np


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


def find_correspondence_left_image(x, offsets):
    """
    Find the corresponding pixel in the left image of a pixel in the result image
    """
    candidates = np.where(np.diff((offsets > x).astype(np.int)) > 0)

    if len(candidates[0]) and len(candidates[0]):
        return candidates[0][-1]
    else:
        return None



def find_correspondence_right_image(x, offsets):
    """
    Find the corresponding pixel in the right image of a pixel in the result image
    """
    candidates = np.where(np.diff((offsets > x).astype(np.int)) > 0)

    if len(candidates) and len(candidates[0]):
        return candidates[0][0]
    else:
        return None


def interpolate_color(source_image_row, x1, x2, factor):
    """
    Get a linear interpolated color
    """
    value1 = source_image_row[x1]
    value2 = source_image_row[x2]
    return np.round(value1*factor + (1-factor)*value2)


def compute_offset_image(disp, direction):
    offset_image = np.zeros(disp.shape, np.float64)

    for y in range(0, len(offset_image)):
        row = offset_image[y]
        disp_row = disp[y]

        for x in range(0, len(row)):
            row[x] = x + direction*disp_row[x]

    return offset_image


def compute_virtual_camera_image_inverse(image_left, image_right, disp_left, disp_right, position):
    """
    Computer an image from a virtual camera by iterating over the result image
    """
    disp_threshold = 7

    virtual_image = np.zeros(image_left.shape, image_left.dtype)
    left_offset = compute_offset_image(disp_left, -position)
    right_offset = compute_offset_image(disp_right, 1-position)

    for y in range(0, len(virtual_image)):
        if y % 36 == 0:
            print(y)

        row = virtual_image[y]
        image_left_row = image_left[y]
        image_right_row = image_right[y]
        left_offset_row = left_offset[y]
        right_offset_row = right_offset[y]

        for x in range(0, len(row)):
            left_id = find_correspondence_left_image(x, left_offset_row)
            # left_id = None
            right_id = find_correspondence_right_image(x, right_offset_row)
            # right_id = None

            diff_left = left_offset_row[left_id+1] - left_offset_row[left_id] if left_id else 999999
            diff_right = right_offset_row[right_id+1] - right_offset_row[right_id] if right_id else 999999

            if diff_left <= disp_threshold:
                color_left = interpolate_color(image_left_row, left_id, left_id + 1,
                                           (left_offset_row[left_id+1] - x) / diff_left)
            if diff_right <= disp_threshold:
                color_right = interpolate_color(image_right_row, right_id, right_id + 1,
                                           (right_offset_row[right_id+1] - x) / diff_right)

            if diff_left > disp_threshold and diff_right > disp_threshold:
                row[x][3] = 255
            elif diff_right > disp_threshold:
                row[x] = color_left
            elif diff_left > disp_threshold:
                row[x] = color_right
            else:
                # row[x] = color_right * x/len(row) + color_left * (1 - x/len(row))
                # row[x] = color_right
                row[x] = color_left


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
