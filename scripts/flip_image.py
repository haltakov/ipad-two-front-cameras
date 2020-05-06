import cv2
import argparse


def parse_args():
    """
    Configures the argument parser
    :return: Parsed arguments
    """

    description = '''Flip an Image horizontally'''

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-i', '--input',
                        dest='input',
                        action='store',
                        required=True,
                        help='Path to the Image to be flipped')

    parser.add_argument('-o', '--output',
                        dest='output',
                        action='store',
                        required=True,
                        help='Path to result flipped image')

    return parser.parse_args()


def main():
    """
    Flips an image
    """

    # Parse the arguments
    args = parse_args()

    # Read the image
    image = cv2.imread(args.input, cv2.IMREAD_UNCHANGED)
    print('Image loaded')

    # Flip
    image_flipped = cv2.flip(image, 1)
    print('Image flipped')

    # Write result
    cv2.imwrite(args.output, image_flipped)
    print('Flipped image written to file.')


if __name__ == "__main__":
    main()
