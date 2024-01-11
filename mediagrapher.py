"""
Main Program
"""

import os
import argparse
from mediagrapher.curves import Curves
from mediagrapher.media.image import ImageMedia
from mediagrapher.grapher.matplotlib_grapher import MatplotlibGrapher

ALLOWED_ALGORITHMS = ["Canny", "Sobel"]

# Argument Parser
parser = argparse.ArgumentParser(
    prog="MediaGrapher",
    description="Command-line interface for graphing images and videos.")

parser.add_argument('url', type=str, help="URL of the image.")
parser.add_argument('-o', '--output', type=str,
                    default="output", help="Output file name.")
parser.add_argument('-a', '--algorithm', type=str,
                    choices=ALLOWED_ALGORITHMS, default="Canny", help="Edge detection algorithm.")
parser.add_argument('-t', '--thresholds', type=int, nargs=2, default=(30, 150), metavar=('LOW', 'HIGH'),
                    help="Thresholds for the Canny edge detection algorithm. (default: 30, 150)")

args = parser.parse_args()

URL = args.url
OUTPUT = args.output
ALGORITHM = args.algorithm
THRESHOLDS = args.thresholds


def main():
    """
    This function is the entry point of the MediaGrapher application.
    It performs the following steps:
    1. Creates an ImageMedia object with a specified URL.
    2. Resizes the image if its resolution is greater than 2000x2000.
    3. Applies the Canny algorithm to detect edges in the image.
    4. Creates a MatplotlibGrapher object with the image resolution.
    5. Checks if the "output" directory exists, and if so, removes it.
    6. Creates a new "output" directory.
    7. Saves the plot with the specified title and file name in the "output" directory.

    Note: This function assumes that the necessary modules and classes are imported.
    """

    image = ImageMedia(url=URL)

    while image.resolution[0] > 1000 or image.resolution[1] > 1000:
        image.resize_scale(0.8)

    curves = Curves(image, algorithm=ALGORITHM, thresholds=THRESHOLDS)
    grapher = MatplotlibGrapher(
        OUTPUT, (image.resolution[0], image.resolution[1]))

    if not os.path.isdir("output"):
        os.mkdir("output")

    grapher.save_plot(1, curves, "output", OUTPUT)


if __name__ == "__main__":
    main()
