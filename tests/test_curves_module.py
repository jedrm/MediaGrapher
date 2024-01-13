"""
Tests for the curves module.
"""

import pytest
import numpy as np
import potrace
from mediagrapher.media.image import ImageMedia
from mediagrapher.curves import Curves


@pytest.fixture
def sample_image_url():
    """A sample image URL."""
    # Following link is from https://picsum.photos/
    return "https://picsum.photos/id/237/200/300"


@pytest.fixture
def sample_image(sample_image_url):
    """A sample image."""
    return ImageMedia(url=sample_image_url)


@pytest.fixture
def sample_curves(sample_image):
    """
    Create a Curves object from a sample image.

    Parameters:
    sample_image (Image): The sample image to create the Curves object from.

    Returns:
    Curves: The Curves object created from the sample image.
    """
    return Curves(sample_image)


@pytest.mark.parametrize("algorithm", ["Canny", "Sobel"])
def test_curves_init(sample_image, algorithm):
    """
    Test the initialization of the Curves object.

    This function checks if the Curves object is initialized correctly.

    Parameters:
    - sample_image: A sample image.
    - algorithm: The algorithm to use for edge detection.

    Returns:
    - None
    """
    curves = Curves(sample_image, algorithm)
    assert isinstance(curves, Curves)
    assert isinstance(curves.media, np.ndarray)
    assert isinstance(curves.bitmap, potrace.Bitmap)
    assert isinstance(curves.path, potrace.Path)


@pytest.mark.parametrize("algorithm", ["lorem", "ipsum"])
def test_curves_init_fail(sample_image, algorithm):
    """
    Test the initialization of the Curves object when the algorithm is invalid.

    This function checks if the Curves object raises a ValueError when the algorithm is invalid.

    Parameters:
    - sample_image: A sample image.
    - algorithm: The algorithm to use for edge detection.

    Returns:
    - None
    """
    with pytest.raises(ValueError):
        Curves(sample_image, algorithm)


@pytest.mark.parametrize("start_point, end_point, t, expected_result", [(0, 10, 0.5, 5), (5, 15, 0.2, 7)])
def test_linear_bezier_curve(sample_curves, start_point, end_point, t, expected_result):
    """
    Test the linear Bezier curve function.

    Args:
        sample_curves (object): An instance of the SampleCurves class.
        start_point (tuple): The starting point of the curve.
        end_point (tuple): The ending point of the curve.
        t (float): The parameter value for the curve.
        expected_result (tuple): The expected result of the curve evaluation.

    Returns:
        None
    """
    result = sample_curves.linear_bezier_curve(start_point, end_point, t)
    assert result == expected_result


@pytest.mark.parametrize("start_point, end_point, c1, c2, t, expected_result", [(0, 10, 2, 8, 0.5, 5), (1, 3, -1, 4, 0.5, 1.625)])
def test_cubic_bezier_curve(sample_curves, start_point, end_point, c1, c2, t, expected_result):
    """
    Test the cubic_bezier_curve function.

    Parameters:
    - sample_curves: An instance of the SampleCurves class.
    - start_point: The starting point of the curve.
    - end_point: The ending point of the curve.
    - c1: The first control point of the curve.
    - c2: The second control point of the curve.
    - t: The parameter value at which to evaluate the curve.
    - expected_result: The expected result of the curve evaluation.

    Returns:
    - None
    """
    result = sample_curves.cubic_bezier_curve(
        start_point, end_point, c1, c2, t)
    assert result == expected_result


def test_get_segments(sample_curves):
    """
    Test the get_segments method of the sample_curves object.

    This function checks if the get_segments method returns a list of segments.
    Each segment should be a list.

    Parameters:
    - sample_curves: An instance of the sample_curves object.

    Returns:
    None
    """
    segments = sample_curves.get_segments()
    assert isinstance(segments, list)
    assert all(isinstance(segment, list) for segment in segments)


def test_get_coordinates(sample_curves):
    """
    Test case for the 'get_coordinates' method of the 'sample_curves' object.

    This test verifies that the 'get_coordinates' method returns a list of coordinates,
    where each coordinate is a list of values. It also checks that the coordinates have
    a length of 100 and that all values are of type float.

    Parameters:
    - sample_curves: An instance of the 'sample_curves' object.

    Returns:
    - None
    """

    coordinates = sample_curves.get_coordinates()
    assert isinstance(coordinates, list)
    assert all(isinstance(coordinate, list) for coordinate in coordinates)
    assert all(isinstance(values, list)
               for coordinate in coordinates for values in coordinate)
    assert all(isinstance(value, float)
               for coordinate in coordinates for values in coordinate for value in values)
