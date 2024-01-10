"""
Matplotlib Grapher Class
"""

from fractions import Fraction
import matplotlib.pyplot as plt
from .grapher import Grapher
from ..curves import Curves


class MatplotlibGrapher(Grapher):
    """
    A class that represents a grapher using Matplotlib library.

    This class provides methods to plot and save graphs using Matplotlib.

    Attributes:
        filename (str): The name of the file to save the graph.
        resolution (tuple): The resolution of the graph in pixels.
        dpi (int): The dots per inch (dpi) of the graph.

    Methods:
        plot(frame: int, curves: Curves, linspace: int = 100) -> None:
            Plots the graph with the given frame, curves, and linspace.

        save_plot(frame: int, curves: Curves, output_dir: str, linspace: int = 100) -> None:
            Saves the current plot to a file in the specified output directory.
    """

    def __init__(self, filename: str, resolution: tuple, dpi: int = 100):
        self.filename = filename
        self.resolution = resolution
        self.dpi = dpi

    def plot(self, frame: int, curves: Curves, linspace: int = 50):
        """
        This method is used to plot the graph.
        It raises a NotImplementedError as it needs to be implemented in the derived class.
        """
        simplified_resolution = Fraction(
            self.resolution[0], self.resolution[1])
        numerator, denominator = simplified_resolution.numerator, simplified_resolution.denominator
        while numerator > 10 or denominator > 10:
            numerator /= 2
            denominator /= 2

        while numerator < 5 or denominator < 5:
            numerator *= 1.5
            denominator *= 1.5

        plt.figure(figsize=(numerator, denominator), dpi=self.dpi)
        plt.title(f'{self.filename}')
        plt.xlabel(f"Frame: {frame}")
        plt.xlim(0, self.resolution[0])
        plt.ylim(0, self.resolution[1])

        curves = curves.get_coordinates(linspace=linspace)
        for curve in curves:
            x, y = curve
            plt.plot(x, y, linewidth=0.5, color='black')
        plt.show()

    def save_plot(self, frame: int, curves: Curves, output_dir: str, output_filename: str, linspace: int = 100):
        """
        Saves the current plot to a file.

        This function is responsible for saving the current plot to a file.
        It can be used to export the plot as an image or any other supported format.

        Raises:
            NotImplementedError: This function is not implemented yet.
        """
        simplified_resolution = Fraction(
            self.resolution[0], self.resolution[1])
        numerator, denominator = simplified_resolution.numerator, simplified_resolution.denominator
        while numerator > 10 or denominator > 10:
            numerator /= 2
            denominator /= 2

        while numerator < 5 or denominator < 5:
            numerator *= 1.5
            denominator *= 1.5

        plt.figure(figsize=(numerator, denominator), dpi=self.dpi)
        plt.title(f'{self.filename}')
        plt.xlabel(f"Frame: {frame}")
        plt.xlim(0, self.resolution[0])
        plt.ylim(0, self.resolution[1])

        curves = curves.get_coordinates(linspace=linspace)
        for curve in curves:
            x, y = curve
            plt.plot(x, y, linewidth=0.5, color='black')

        plt.savefig(f'{output_dir}/{output_filename}.png')
