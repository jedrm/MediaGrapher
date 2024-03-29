"""
Main Program
"""

import os
import argparse
import glob
import yt_dlp
import ffmpeg
from tqdm import trange
from joblib import Parallel, delayed
from mediagrapher.curves import Curves
from mediagrapher.media.image import ImageMedia
from mediagrapher.grapher.matplotlib_grapher import MatplotlibGrapher

ALLOWED_ALGORITHMS = ["Canny", "Sobel"]
MAX_THREADS = os.cpu_count()

# Argument Parser
parser = argparse.ArgumentParser(
    prog="MediaGrapher",
    description="Command-line interface for graphing images and videos.")

parser.add_argument('url', type=str, help="URL of the image.")
parser.add_argument('-o', '--output', type=str,
                    default="output", help="Output file name.")
parser.add_argument('-a', '--algorithm', type=str,
                    choices=ALLOWED_ALGORITHMS, default="Canny", help="Edge detection algorithm.")
parser.add_argument('-t', '--thresholds', type=int, nargs=2, default=(30, 200), metavar=('LOW', 'HIGH'),
                    help="Thresholds for the Canny edge detection algorithm. (default: 30, 200)")
parser.add_argument('-p', '--threads', type=int, choices=range(1, MAX_THREADS+1), default=MAX_THREADS,
                    help="Number of threads utilized on the CPU. (default: MAX_THREADS)")
args = parser.parse_args()

URL = args.url
OUTPUT = args.output
ALGORITHM = args.algorithm
THRESHOLDS = args.thresholds
THREADS = args.threads

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
            'outtmpl': os.path.join("input", "input.") + '%(ext)s',
            'merge_output_format': 'mp4',
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        return ("video", "input/input.mp4")
    except yt_dlp.utils.DownloadError:
        return ("error", "Invalid URL.")


def process_image(image: ImageMedia, title: str, frame: int = 1, output: str = "output", algorithm: str = "Canny", thresholds: tuple = (30, 150)):
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

    os.makedirs("output", exist_ok=True)
    os.makedirs(os.path.join("output", "frames"), exist_ok=True)

    grapher.save_plot(frame, curves, "output", output, title)


def process_frame(frame: int, frames_folder: str, output_filename: str):
    """
    Process a single frame of an image.

    Args:
        frame (int): The frame number to process.
        frames_folder (str): The folder path where the frames are stored.
        output_filename (str): The filename of the output image.

    Returns:
        None
    """
    image = ImageMedia(filename=os.path.join(frames_folder, f"frame_{frame}.jpg"))
    process_image(image, output_filename, frame=frame, output=os.path.join(
        'frames', f"frame_{frame}"))


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


def combine_video_frames(video_path: str, frames_folder: str, output_path: str, fps: int):
    """
    Combines individual frames into a video file.

    Args:
        frames_folder (str): The folder containing the frames.
        output_path (str): The path to the output video file.
        fps (int): The frames per second of the video.

    Returns:
        None
    """
    audio = ffmpeg.input(video_path).audio
    (
        ffmpeg.input(os.path.join(
            frames_folder, "frame_%d.png"), framerate=fps)
        .output(audio, output_path)
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
            'fps': int(video_info['avg_frame_rate'].split('/')[0]) / int(video_info['avg_frame_rate'].split('/')[1]),
            'width': int(video_info['width']),
            'height': int(video_info['height']),
            'codec_name': video_info['codec_name'],
            'total_frames': video_info['nb_frames']
        }
        return metadata
    except ffmpeg.Error as e:
        print(f"Error: {e.stderr.decode('utf-8')}")
        return None


def process_video(video_path: str, frames_folder: str, output_filename: str, threads: int):
    """
    Process a video by extracting frames, applying image processing algorithms to each frame, and combining the processed frames into a new video.

    Args:
        video_path (str): The path to the input video file.
        frames_folder (str): The folder to store the extracted frames.
        output_folder (str): The folder to store the output video and processed frames.
        algorithm (str, optional): The image processing algorithm to apply to each frame. Defaults to "Canny".
        thresholds (tuple, optional): The thresholds to be used by the image processing algorithm. Defaults to (30, 150).
    """
    print(f"Utilizing {threads} threads...")
    print("Getting video metadata...")
    metadata = get_video_metadata(video_path)

    print("Extracting frames...")
    os.makedirs(frames_folder, exist_ok=True)
    get_video_frames(video_path, frames_folder)

    print("Processing frames...")

    total_frames = int(metadata['total_frames'])
    Parallel(n_jobs=threads)(delayed(process_frame)(frame, frames_folder, output_filename) for frame in trange(1, total_frames + 1))

    print("Combining frames...")
    combine_video_frames(video_path, os.path.join(
        'output', 'frames'), os.path.join('output', f'{output_filename}.mp4'), metadata['fps'])
    print("Done.")


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

    input_frames = os.path.join("input", "frames")
    output_frames = os.path.join("output", "frames")

    os.makedirs(input_frames, exist_ok=True)
    os.makedirs(output_frames, exist_ok=True)

    input_dir = glob.glob(os.path.join("input", "*.mp4"))
    input_frames = glob.glob(os.path.join(input_frames, "*"))
    output_frames = glob.glob(os.path.join(output_frames, "*"))

    for input_file in input_dir:
        os.remove(input_file)
    for input_frame in input_frames:
        os.remove(input_frame)
    for output_frame in output_frames:
        os.remove(output_frame)

    media_type, media = get_media(URL)
    if media_type == "image":
        print("Processing image...")
        process_image(media, OUTPUT, 1, OUTPUT, ALGORITHM, THRESHOLDS)
        print("Done.")
    elif media_type == "video":
        print("Processing video...")
        process_video(media, os.path.join("input", "frames"), OUTPUT, THREADS)
    else:
        print("Error: Could not process media.")


if __name__ == "__main__":
    main()
