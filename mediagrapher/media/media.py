"""
Media Class
"""

import abc
import numpy as np


class Media(metaclass=abc.ABCMeta):
    """
    Abstract base class for representing media objects.

    Attributes:
        - url (str): The URL of the media.
        - filename (str): The filename of the media.
        - resolution: The resolution of the media (None by default).
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_data_source') and
                callable(subclass.load_data_source) and
                hasattr(subclass, 'extract_text') and
                callable(subclass.extract_text) or
                NotImplemented)

    def __init__(self, url: str, filename: str):
        """
        Initialize a Media object.

        Args:
            url (str): The URL of the media.
            filename (str): The filename of the media.
        """
        self.url = url
        self.filename = filename
        self.resolution = None

    @abc.abstractmethod
    def __str__(self) -> str:
        """
        Returns a string representation of the Media object.

        Returns:
            str: The string representation of the Media object.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def to_numpy_array(self) -> np.ndarray:
        """
        Converts the media object to a NumPy array.

        Returns:
            np.ndarray: The media object as a NumPy array.
        """
        raise NotImplementedError

    @abc.abstractmethod
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

    @abc.abstractmethod
    def get_sobel(self) -> np.ndarray:
        """
        Apply Sobel edge detection to the image.

        Returns:
            np.ndarray: The resulting image after applying Sobel edge detection.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def resize_resolution(self, width: int, height: int) -> None:
        """
        Resizes the media object to the specified resolution.

        Args:
            width (int): The new width of the media object.
            height (int): The new height of the media object.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def resize_scale(self, scale: float) -> None:
        """
        Resizes the media object by the specified scale factor.

        Args:
            scale (float): The scale factor to resize the media object.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def rotate(self, angle: float) -> None:
        """
        Rotates the media object by the specified angle.

        Args:
            angle (float): The angle in degrees to rotate the media object.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def flip_image(self) -> None:
        """
        Flips the media object horizontally.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def change_format(self, new_format: str) -> None:
        """
        Changes the format of the media object to the specified format.

        Args:
            new_format (str): The new format of the media object.
        """
        raise NotImplementedError
