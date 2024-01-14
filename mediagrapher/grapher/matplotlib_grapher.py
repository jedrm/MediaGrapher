"""
Matplotlib Grapher Class
"""

from fractions import Fraction
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.path as mpath
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
        plot(frame: int, curves: Curves, linspace: int = 50) -> None:
            Plots the graph with the given frame, curves, and linspace.

        save_plot(frame: int, curves: Curves, output_dir: str, linspace: int = 50) -> None:
            Saves the current plot to a file in the specified output directory.
    """

    def __init__(self, filename: str, resolution: tuple, dpi: int = 100):
        self.filename = filename
        self.resolution = resolution
        self.dpi = dpi

    def plot(self, frame: int, curves: Curves, title: str, linspace: int = 50):
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

        _, ax = plt.subplots(figsize=(numerator, denominator), dpi=self.dpi)
        ax.set_title(title)
        ax.set_xlabel(f"Frame: {frame}")
        ax.set_xlim(0, self.resolution[0])
        ax.set_ylim(0, self.resolution[1])

        curves = curves.get_segments()
        Path = mpath.Path
        for curve in curves:
            if len(curve) == 4:
                path_curve = Path(
                    curve, [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4])
            else:
                path_curve = Path(curve, [Path.MOVETO, Path.LINETO])
            path_patch = mpatches.PathPatch(
                path_curve, aa=None, fc="none", ec=None, lw=0.5)
            ax.add_patch(path_patch)

        plt.show()

    def save_plot(self, frame: int, curves: Curves, output_dir: str, output_filename: str, title: str, linspace: int = 50):
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

        _, ax = plt.subplots(figsize=(numerator, denominator), dpi=self.dpi)
        ax.set_title(title)
        ax.set_xlabel(f"Frame: {frame}")
        ax.set_xlim(0, self.resolution[0])
        ax.set_ylim(0, self.resolution[1])

        curves = curves.get_segments()
        Path = mpath.Path
        for curve in curves:
            if len(curve) == 4:
                path_curve = Path(
                    curve, [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4])
            else:
                path_curve = Path(curve, [Path.MOVETO, Path.LINETO])
            path_patch = mpatches.PathPatch(
                path_curve, aa=None, fc="none", ec=None, lw=0.5)
            ax.add_patch(path_patch)

        plt.savefig(f'{output_dir}/{output_filename}.png')
        plt.close()
