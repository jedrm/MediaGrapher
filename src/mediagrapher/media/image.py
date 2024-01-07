"""
Image Class
"""

import numpy as np
import cv2
from PIL import Image
from .media import Media


class ImageMedia(Media):
    """
    Represents an image object.
    """

    def __init__(self, url, filename):
        """
        Initializes the Image object.
        """
        super().__init__(url, filename)
        self.image = Image.open(f"frames/{filename}")
        self.resolution = self.image.size

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

    def get_canny(self, low_threshold, high_threshold) -> np.ndarray:
        """
        Apply Canny edge detection to the image.

        Args:
            low_threshold (int): The lower threshold value for the hysteresis procedure.
            high_threshold (int): The higher threshold value for the hysteresis procedure.

        Returns:
            np.ndarray: The resulting image after applying Canny edge detection.
        """
        return cv2.Canny(self.to_numpy_array(), low_threshold, high_threshold)

    def get_sobel(self) -> np.ndarray:
        """
        Apply Sobel edge detection to the image.

        Returns:
            np.ndarray: The resulting image after applying Sobel edge detection.
        """
        scale = 1
        delta = 0
        ddepth = cv2.CV_16S

        src = cv2.imread(self.filename, cv2.IMREAD_COLOR)
        src = cv2.GaussianBlur(src, (3, 3), 0)
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

    def resize_scale(self, scale: float) -> None:
        """
        Resizes the image object by the specified scale factor.

        Args:
            scale (float): The scale factor to resize the image object.
        """
        self.image = self.image.resize(
            (int(self.resolution[0] * scale), int(self.resolution[1] * scale)))

    def rotate(self, angle: float) -> None:
        """
        Rotates the image object by the specified angle.

        Args:
            angle (float): The angle in degrees to rotate the image object.
        """
        self.image = self.image.rotate(angle)

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
