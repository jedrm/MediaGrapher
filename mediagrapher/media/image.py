"""
Image Class
"""

import os
from io import BytesIO

import numpy as np
import cv2
import requests
from PIL import Image, ImageOps
from .media import Media


class ImageMedia(Media):
    """
    Represents an image media object.

    Attributes:
        - url (str): The URL of the image.
        - filename (str): The filename of the image.
        - image (PIL.Image.Image): The image object.
        - resolution (tuple): The resolution of the image (width, height).

    Methods:
        - __init__(self, url=None, filename=None): Initializes the ImageMedia object.
        - __str__(self) -> str: Returns a string representation of the ImageMedia object.
        - to_numpy_array(self) -> np.ndarray: Converts the image object to a NumPy array.
        - get_canny(self, low_threshold, high_threshold) -> np.ndarray: Applies Canny edge detection to the image.
        - get_sobel(self) -> np.ndarray: Applies Sobel edge detection to the image.
        - resize_resolution(self, width: int, height: int) -> None: Resizes the image object to the specified resolution.
        - resize_scale(self, scale: float) -> None: Resizes the image object by the specified scale factor.
        - rotate(self, angle: float) -> None: Rotates the image object by the specified angle.
        - change_format(self, new_format: str) -> None: Changes the format of the image object to the specified format.
        - convert_to_png(self) -> np.ndarray: Changes the image to a transparent PNG and only keeps the original subject.
    """

    def __init__(self, url=None, filename=None):
        """
        Initializes the ImageMedia object.

        Args:
            url (str): The URL of the image.
            filename (str): The filename of the image.

        Raises:
            ValueError: If neither url nor filename is provided.
            ValueError: If the URL does not exist or is not accessible.
            ValueError: If the URL is not a valid image file.
            FileNotFoundError: If the file does not exist in the current directory.
        """
        if not (url or filename):
            raise ValueError("Either url or filename must be provided")

        # Check if the file exists, if not, download from internet
        super().__init__(url, filename)
        if url:
            try:
                response = requests.get(url, allow_redirects=True, timeout=10)
            except requests.exceptions.ConnectionError as e:
                raise ValueError(
                    f"URL {url} does not exist or is not accessible") from e

            if not response.ok:
                raise ValueError(
                    f"URL {url} does not exist or is not accessible")

            content_type = response.headers.get('content-type')
            if 'image' not in content_type:
                raise ValueError(
                    f"URL {url} is not a valid image file")

            self.image = Image.open(BytesIO(response.content))
            self.resolution = self.image.size

        else:
            if not os.path.isfile(filename):
                raise FileNotFoundError(
                    f"File {filename} does not exist in the current directory")
            self.image = Image.open(filename)
            self.resolution = self.image.size

        self.rotate(180)
        self.flip_image()

    def __str__(self) -> str:
        """
        Returns a string representation of the Image object.

        Returns:
            str: The string representation of the Image object.
        """
        return f"ImageMedia(url={self.url}, filename={self.filename}), resolution={self.resolution}"

    def to_numpy_array(self) -> np.ndarray:
        """
        Converts the image object to a NumPy array.

        Returns:
            np.ndarray: The image object as a NumPy array.
        """
        return np.array(self.image)

    def get_canny(self, low_threshold: int = 50, high_threshold: int = 150) -> np.ndarray:
        """
        Apply Canny edge detection to the image.

        Args:
            low_threshold (int): The lower threshold value for the hysteresis procedure.
            high_threshold (int): The higher threshold value for the hysteresis procedure.

        Returns:
            np.ndarray: The resulting image after applying Canny edge detection.
        """
        src = self.to_numpy_array()
        src = cv2.GaussianBlur(src, (3, 3), 0)
        return cv2.Canny(src, low_threshold, high_threshold)

    def get_sobel(self) -> np.ndarray:
        """
        Apply Sobel edge detection to the image.

        Returns:
            np.ndarray: The resulting image after applying Sobel edge detection.
        """
        scale = 1
        delta = 0
        ddepth = cv2.CV_16S

        src = cv2.GaussianBlur(self.to_numpy_array(), (3, 3), 0)
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

        grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale,
                           delta=delta, borderType=cv2.BORDER_DEFAULT)
        grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale,
                           delta=delta, borderType=cv2.BORDER_DEFAULT)

        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)

        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        return grad

    def resize_resolution(self, width: int, height: int) -> None:
        """
        Resizes the image object to the specified resolution.

        Args:
            width (int): The new width of the image object.
            height (int): The new height of the image object.
        """
        self.image = self.image.resize((width, height))
        self.resolution = self.image.size

    def resize_scale(self, scale: float) -> None:
        """
        Resizes the image object by the specified scale factor.

        Args:
            scale (float): The scale factor to resize the image object.
        """
        self.image = self.image.resize(
            (int(self.resolution[0] * scale), int(self.resolution[1] * scale)))
        self.resolution = self.image.size

    def rotate(self, angle: float) -> None:
        """
        Rotates the image object by the specified angle.

        Args:
            angle (float): The angle in degrees to rotate the image object.
        """
        self.image = self.image.rotate(angle)
        self.resolution = self.image.size

    def flip_image(self) -> None:
        """
        Flips the image horizontally (left to right).

        This method uses the `transpose` function from the `PIL.Image` module
        to flip the image horizontally. It updates the `image` attribute and
        the `resolution` attribute with the new flipped image and its size
        respectively.
        """
        self.image = ImageOps.mirror(self.image)
        self.resolution = self.image.size

    def change_format(self, new_format: str) -> None:
        """
        Changes the format of the image object to the specified format.

        Args:
            new_format (str): The new format of the image object.
        """
        raise NotImplementedError

    def convert_to_png(self) -> np.ndarray:
        """
        Changes the image to a transparent PNG and only keep the original subject

        Returns:
            np.ndarray: The resulting image after applying the conversion.
        """
        raise NotImplementedError
