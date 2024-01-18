"""
Curves class
"""

from typing import List, Tuple
import numpy as np
import potrace
from .media.media import Media


class Curves:
    """
    Represents a collection of curves extracted from a media object.

    The Curves class provides methods to retrieve segments and coordinates of the curves in the path.
    It also includes functions to calculate linear and cubic Bezier curves.

    Attributes:
        media (Media): The media object.
        bitmap (potrace.Bitmap): The bitmap representation of the media.
        path (potrace.Path): The traced path of the curves.

    Methods:
        __init__(self, media: Media, algorithm: str = "Canny"): Initializes the Curves object.
        get_segments(self) -> List[List[Tuple[float, float]]]: Returns a list of segments in the path.
        get_coordinates(self, linspace: int = 50) -> List[List[List[float]]]: Returns the coordinates of the curves in the path.
        linear_bezier_curve(self, start_point: int, end_point: int, t: float) -> float: Calculates the linear Bezier curve.
        cubic_bezier_curve(self, start_point: int, end_point: int, c1: int, c2: int, t: float) -> float: Calculates the cubic Bezier curve.
    """

    def __init__(self, media: Media, algorithm: str = "Canny", thresholds: Tuple[int, int] = (50, 150)):
        """
        Initializes the Curves object.

        Args:
            media (Media): The media object.
            algorithm (str): The algorithm to use for curve extraction. Default is "Canny".
                Valid options are "Canny" and "Sobel".

        Raises:
            ValueError: If an invalid algorithm is provided.
        """
        match algorithm:
            case "Canny":
                self.media = media.get_canny(low_threshold=thresholds[0], high_threshold=thresholds[1])
            case "Sobel":
                self.media = media.get_sobel()
            case _:
                raise ValueError("Invalid algorithm.")

        for i, _ in enumerate(self.media):
            self.media[i][self.media[i] > 1] = 1

        self.bitmap = potrace.Bitmap(self.media)
        self.path = self.bitmap.trace()

    def get_segments(self) -> List[List[Tuple[float, float]]]:
        """
        Returns a list of segments in the path, where each segment is represented as a list of integers.

        Each segment consists of a start point, an end point, and control points (if applicable).
        If the segment is a corner, it will have a single control point 'c'.
        If the segment is a curve, it will have two control points 'c1' and 'c2'.

        Returns:
            List[List[float]]: A list of segments, where each segment is represented as a list of integers.
        """
        segments = []
        for curve in self.path:
            start_point = curve.start_point
            for segment in curve:
                end_point = segment.end_point
                if segment.is_corner:
                    c = segment.c
                    segments.append([start_point, c])
                    segments.append([c, end_point])
                else:
                    c1 = segment.c1
                    c2 = segment.c2
                    segments.append([start_point, c1, c2, end_point])
                start_point = segment.end_point
        return segments

    def get_coordinates(self, linspace: int = 50) -> List[List[List[float]]]:
        """
        Returns the coordinates of the curves in the path.

        Args:
            linspace (int): The number of points to generate along each curve segment. Default is 100.

        Returns:
            List[List[List[float], List[float]]]: A list of coordinates for each curve segment in the path.
                Each coordinate is represented as a list of x and y values.
        """
        coordinates = []

        for curve in self.path:
            start_x, start_y = curve.start_point
            start_x, start_y = [start_x] * linspace, [start_y] * linspace

            for segment in curve:
                if segment.is_corner:
                    c_x, c_y = segment.c
                    end_x, end_y = segment.end_point

                    c_x, c_y = [c_x] * linspace, [c_y] * linspace
                    end_x, end_y = [end_x] * linspace, [end_y] * linspace

                    t = np.linspace(0, 1, linspace)

                    first_line_x = list(map(
                        self.linear_bezier_curve, start_x, c_x, t))
                    first_line_y = list(map(
                        self.linear_bezier_curve, start_y, c_y, t))

                    second_line_x = list(map(
                        self.linear_bezier_curve, c_x, end_x, t))
                    second_line_y = list(map(
                        self.linear_bezier_curve, c_y, end_y, t))

                    coordinates.append([first_line_x, first_line_y])
                    coordinates.append([second_line_x, second_line_y])

                else:
                    c1_x, c1_y = segment.c1
                    c2_x, c2_y = segment.c2
                    end_x, end_y = segment.end_point

                    c1_x, c1_y = [c1_x] * linspace, [c1_y] * linspace
                    c2_x, c2_y = [c2_x] * linspace, [c2_y] * linspace
                    end_x, end_y = [end_x] * linspace, [end_y] * linspace

                    t = np.linspace(0, 1, linspace)

                    curve_x = list(map(self.cubic_bezier_curve,
                                       start_x, c1_x, c2_x, end_x, t))
                    curve_y = list(map(self.cubic_bezier_curve,
                                       start_y, c1_y, c2_y, end_y, t))

                    coordinates.append([curve_x, curve_y])
                start_x, start_y = end_x, end_y
        return coordinates

    def linear_bezier_curve(self, start_point: int, end_point: int, t: float) -> float:
        """
        Returns the linear Bezier curve.

        Args:
            start_point (int): The start point.
            end_point (int): The end point.
            t (float): The t value.

        Returns:
            int: The linear Bezier curve.
        """
        return (1 - t) * start_point + t * end_point

    def cubic_bezier_curve(self, start_point: int, c1: int, c2: int, end_point: int, t: float) -> float:
        """
        Returns the cubic Bezier curve.

        Args:
            start_point (int): The start point.
            end_point (int): The end point.
            c1 (int): The first control point.
            c2 (int): The second control point.
            t (float): The t value.

        Returns:
            int: The cubic Bezier curve.
        """
        return (1 - t) ** 3 * start_point + 3 * (1 - t) ** 2 * t * c1 + 3 * (1 - t) * t ** 2 * c2 + t ** 3 * end_point
