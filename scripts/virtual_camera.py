import numpy as np


def compute_offset_image(disp, direction):
    """
    Compute an image containing the precomputed offsets from the disparity map
    """
    offset_image = np.zeros(disp.shape, np.float64)

    for y in range(0, len(offset_image)):
        row = offset_image[y]
        disp_row = disp[y]

        for x in range(0, len(row)):
            row[x] = x + direction*disp_row[x]

    return offset_image


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


def compute_virtual_camera_image_inverse(image_left, image_right, disp_left, disp_right, position):
    """
    Computer an image from a virtual camera by iterating over the result image
    """
    # Threshold for the maximum disparity which will be used to fill the pixel.
    disp_threshold = 7

    virtual_image = np.zeros(image_left.shape, image_left.dtype)

    # Precompute the offset images
    left_offset = compute_offset_image(disp_left, -position)
    right_offset = compute_offset_image(disp_right, 1-position)

    # Iterate over all pixels of the result image
    for y in range(0, len(virtual_image)):
        row = virtual_image[y]
        image_left_row = image_left[y]
        image_right_row = image_right[y]
        left_offset_row = left_offset[y]
        right_offset_row = right_offset[y]

        # Iterate over the pixels of a row
        for x in range(0, len(row)):
            # Find the correspondences in the left and in the right image
            left_id = find_correspondence_left_image(x, left_offset_row)
            # Uncomment if you want to get only the right image with "shadows"
            # left_id = None
            right_id = find_correspondence_right_image(x, right_offset_row)
            # Uncomment if you want to get only the left image with "shadows"
            # right_id = None

            diff_left = left_offset_row[left_id+1] - left_offset_row[left_id] if left_id else 999999
            diff_right = right_offset_row[right_id+1] - right_offset_row[right_id] if right_id else 999999

            # Compute the color from the left and from the right image
            if diff_left <= disp_threshold:
                color_left = interpolate_color(image_left_row, left_id, left_id + 1,
                                           (left_offset_row[left_id+1] - x) / diff_left)
            if diff_right <= disp_threshold:
                color_right = interpolate_color(image_right_row, right_id, right_id + 1,
                                           (right_offset_row[right_id+1] - x) / diff_right)

            # Choose if the color from the left or the right image should be used
            if diff_left > disp_threshold and diff_right > disp_threshold:
                row[x][3] = 255
            elif diff_right > disp_threshold:
                row[x] = color_left
            elif diff_left > disp_threshold:
                row[x] = color_right
            else:
                # I tried different ways of combining the images here
                # row[x] = color_right * x/len(row) + color_left * (1 - x/len(row))
                # row[x] = color_right
                row[x] = color_left

    return virtual_image


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

