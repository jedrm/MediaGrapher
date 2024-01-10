"""
Grapher Class
"""

import abc
from ..curves import Curves


class Grapher(metaclass=abc.ABCMeta):
    """
    The Grapher class is an abstract base class that defines the interface for graphing operations.

    This class provides the common methods and attributes that any derived graphing class should implement.
    It cannot be instantiated directly and must be subclassed to create a concrete graphing class.

    Attributes:
        filename (str): The name of the file to save the plot.
        resolution (tuple): The resolution of the plot.

    Methods:
        plot(): Abstract method to plot the graph.
        save_plot(): Abstract method to save the plot to a file.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_data_source') and
                callable(subclass.load_data_source) and
                hasattr(subclass, 'extract_text') and
                callable(subclass.extract_text) or
                NotImplemented)

    @abc.abstractmethod
    def __init__(self, filename: str, resolution: tuple):
        raise NotImplementedError

    @abc.abstractmethod
    def plot(self, frame: int, curves: Curves, linspace: int = 100):
        """
        This method is used to plot the graph.
        It raises a NotImplementedError as it needs to be implemented in the derived class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def save_plot(self, frame: int, curves: Curves, output_dir: str, linspace: int = 100):
        """
        Saves the current plot to a file.

        This function is responsible for saving the current plot to a file.
        It can be used to export the plot as an image or any other supported format.

        Raises:
            NotImplementedError: This function is not implemented yet.
        """
        raise NotImplementedError
