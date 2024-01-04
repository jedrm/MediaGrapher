"""
Image Class
"""

import numpy as np
import requests
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
        response = requests.head(url, allow_redirects=True, timeout=10)

        if response.status_code == 200:
            with open(f"frames/{filename}", 'wb') as file:
                file.write(response.content)

        image = Image.open(f"frames/{filename}")
        self.image_array = np.array(image)

    def __str__(self) -> str:
        """
        Returns a string representation of the Image object.

        Returns:
            str: The string representation of the Image object.
        """
        return f"ImageMedia(url={self.url}, filename={self.filename})"

    def to_numpy_array(self) -> np.ndarray:
        """
        Converts the image object to a NumPy array.

        Returns:
            np.ndarray: The image object as a NumPy array.
        """
        return self.image_array

    def get_canny(self, low_threshold, high_threshold) -> np.ndarray:
        """
        Apply Canny edge detection to the image.

        Args:
            low_threshold (int): The lower threshold value for the hysteresis procedure.
            high_threshold (int): The higher threshold value for the hysteresis procedure.

        Returns:
            np.ndarray: The resulting image after applying Canny edge detection.
        """
        raise NotImplementedError

    def get_sobel(self) -> np.ndarray:
        """
        Apply Sobel edge detection to the image.

        Returns:
            np.ndarray: The resulting image after applying Sobel edge detection.
        """
        raise NotImplementedError

    def resize_resolution(self, width: int, height: int) -> None:
        """
        Resizes the image object to the specified resolution.

        Args:
            width (int): The new width of the image object.
            height (int): The new height of the image object.
        """
        raise NotImplementedError

    def resize_scale(self, scale: float) -> None:
        """
        Resizes the image object by the specified scale factor.

        Args:
            scale (float): The scale factor to resize the image object.
        """
        raise NotImplementedError

    def rotate(self, angle: float) -> None:
        """
        Rotates the image object by the specified angle.

        Args:
            angle (float): The angle in degrees to rotate the image object.
        """
        raise NotImplementedError

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
