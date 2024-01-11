"""
Main Program
"""

import os
from mediagrapher.curves import Curves
from mediagrapher.grapher.matplotlib_grapher import MatplotlibGrapher
from mediagrapher.media.image import ImageMedia


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

    image = ImageMedia(
        url="https://www.allkpop.com/upload/2023/07/content/061258/1688662714-newjeans-new-jeans-official-mv-1-30-screenshot.png")

    while image.resolution[0] > 2000 or image.resolution[1] > 2000:
        image.resize_scale(0.75)

    curves = Curves(image, algorithm="Canny", thresholds=(30, 150))
    grapher = MatplotlibGrapher(
        "test", (image.resolution[0], image.resolution[1]))

    if os.path.isdir("output"):
        os.rmdir("output")
    os.mkdir("output")
    grapher.save_plot(1, curves, "output", "Powerpuff Girls")


if __name__ == "__main__":
    main()
