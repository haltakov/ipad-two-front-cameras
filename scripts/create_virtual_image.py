import os
import cv2
import argparse
from virtual_camera import compute_virtual_camera_image, fill_holes


def parse_args():
    """
    Configures the argument parser
    :return: Parsed arguments
    """

    description = '''Flip a disparity map horizntally'''

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-i', '--input',
                        dest='input',
                        action='store',
                        required=True,
                        help='Path to a folder containing the input images')

    parser.add_argument('-p', '--path',
                        dest='path',
                        action='store',
                        required=True,
                        help='Path to the file where the virtual image should be stored')

    parser.add_argument('-o', '--offset',
                        dest='offset',
                        action='store',
                        default=0.5,
                        help='Offset between the two images (value between 0 and 1)')

    parser.add_argument('-d', '--display',
                        dest='display',
                        action='store_true',
                        help='Display the computed image')

    return parser.parse_args()


def main():
    """
    Computes a virtual image form a stereo pair
    """

    # Parse the arguments
    args = parse_args()
    offset = float(args.offset)

    # Read the images
    image_left = cv2.imread(os.path.join(args.input, 'image_left.png'), cv2.IMREAD_UNCHANGED)
    image_right = cv2.imread(os.path.join(args.input, 'image_right.png'), cv2.IMREAD_UNCHANGED)
    disp_left = cv2.imread(os.path.join(args.input, 'disp_left.png'), cv2.IMREAD_UNCHANGED)
    disp_right = cv2.imread(os.path.join(args.input, 'disp_right.png'), cv2.IMREAD_UNCHANGED)
    print('Images loaded')

    # Prepare disparity maps
    disp_left = disp_left / 256.0
    disp_right = disp_right / 256.0
    fill_holes(disp_left)
    fill_holes(disp_right)

    # Compute the virtual image
    virtual_image = compute_virtual_camera_image(image_left, image_right, disp_left, disp_right, offset)
    print('Virtual image computed')

    # Write result
    cv2.imwrite(args.path, virtual_image)
    print('Virtual image written to file')

    # Display the image
    if args.display:
        cv2.imshow('Virtual image', virtual_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()