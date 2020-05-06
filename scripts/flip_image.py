import cv2
import argparse


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
                        help='Path to the disparity map to be flipped')

    parser.add_argument('-o', '--output',
                        dest='output',
                        action='store',
                        required=True,
                        help='Path to result flipped disparity map')

    return parser.parse_args()


def main():
    """
    Flips the disparity map
    """

    # Parse the arguments
    args = parse_args()

    # Read the image
    disparity_map = cv2.imread(args.input, cv2.IMREAD_UNCHANGED)
    print('Disparity map loaded')

    # Flip
    disparity_map_flipped = cv2.flip(disparity_map, 1)
    print('Disparity map flipped')

    # Write result
    cv2.imwrite(args.output, disparity_map_flipped)
    print('Flipped disparity map written to file.')


if __name__ == "__main__":
    main()