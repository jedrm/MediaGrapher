"""
Main Program
"""

import os
import argparse
import yt_dlp
import ffmpeg
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


def get_media(url: str) -> tuple:
    """
    Retrieves media from a given URL.

    Args:
        url (str): The URL of the media.

    Returns:
        tuple: A tuple containing the type of media ('image' or 'video') and the media itself.
               If the URL is invalid, it returns a tuple with the type 'error' and an error message.
    """
    try:
        return ("image", ImageMedia(url=url))
    except ValueError:
        pass
    try:
        options = {
            'format': 'best',
            'outtmpl': 'input/input.' + '%(ext)s',
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download(['https://www.youtube.com/watch?v=Mmp-NcbA9PU'])

        return ("video", "input/input.mp4")
    except yt_dlp.utils.DownloadError:
        return ("error", "Invalid URL.")


def process_image(image: ImageMedia, frame: int = 1, output: str = "output", algorithm: str = "Canny", thresholds: tuple = (30, 150)):
    """
    Process an image using the specified algorithm and save the resulting plot.

    Args:
        image (ImageMedia): The input image to be processed.
        frame (int, optional): The frame number of the image. Defaults to 1.
        output (str, optional): The output directory to save the plot. Defaults to "output".
        algorithm (str, optional): The algorithm to be used for processing the image. Defaults to "Canny".
        thresholds (tuple, optional): The thresholds to be used for the algorithm. Defaults to (30, 150).
    """

    while image.resolution[0] > 1000 or image.resolution[1] > 1000:
        image.resize_scale(0.8)

    curves = Curves(image, algorithm=algorithm, thresholds=thresholds)
    grapher = MatplotlibGrapher(
        output, (image.resolution[0], image.resolution[1]))

    if not os.path.isdir("output"):
        os.mkdir("output")

    grapher.save_plot(frame, curves, "output", output)


def get_video_frames(video_path: str, output_folder: str):
    """
    Extracts frames from a video file and saves them as individual images.

    Args:
        video_path (str): The path to the video file.
        output_folder (str): The folder where the extracted frames will be saved.

    Returns:
        None
    """
    os.makedirs(output_folder, exist_ok=True)

    (
        ffmpeg.input(video_path)
        .output(os.path.join(output_folder, 'frame_%d.jpg'), start_number=1)
        .overwrite_output()
        .run(quiet=True)
    )


def get_video_metadata(video_path):
    """
    Retrieves metadata for a video file.

    Args:
        video_path (str): The path to the video file.

    Returns:
        dict: A dictionary containing the following metadata:
            - 'duration': The duration of the video in seconds (float).
            - 'fps': The frames per second of the video (int).
            - 'width': The width of the video in pixels (int).
            - 'height': The height of the video in pixels (int).
            - 'codec_name': The name of the video codec (str).

    Raises:
        ffmpeg.Error: If an error occurs while probing the video file.
    """
    try:
        probe = ffmpeg.probe(video_path)
        video_info = next(
            s for s in probe['streams'] if s['codec_type'] == 'video')
        metadata = {
            'duration': float(video_info['duration']),
            'fps': int(video_info['avg_frame_rate'].split('/')[0]) // int(video_info['avg_frame_rate'].split('/')[1]),
            'width': int(video_info['width']),
            'height': int(video_info['height']),
            'codec_name': video_info['codec_name'],
        }
        return metadata
    except ffmpeg.Error as e:
        print(f"Error: {e.stderr.decode('utf-8')}")
        return None


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
    process_image(image, 1, OUTPUT, ALGORITHM, THRESHOLDS)


if __name__ == "__main__":
    main()
