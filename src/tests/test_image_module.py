"""
Testing the mediagrapher module.
"""

import os
import pytest
import numpy as np
from mediagrapher.media.image import ImageMedia


TEST_IMAGE_DIR = os.path.join("src", "tests", "test_images")


@pytest.fixture
def sample_image_url():
    """A sample image URL."""
    # Following link is from https://picsum.photos/
    return "https://picsum.photos/id/237/200/300"


@pytest.fixture
def sample_filename():
    """A sample image filename."""
    return os.path.join(TEST_IMAGE_DIR, "730.jpg")


@pytest.fixture
def sample_image(sample_image_url):
    """A sample image."""
    return ImageMedia(url=sample_image_url)


@pytest.fixture
def sample_image_from_file(sample_filename):
    """A sample image from file."""
    return ImageMedia(filename=sample_filename)


def test_image_file_does_not_exist():
    """
    Test the ImageMedia class when the image file does not exist.

    Returns:
        None
    """
    with pytest.raises(FileNotFoundError):
        ImageMedia(filename="non_existent_file.jpg")


def test_image_url_is_invalid():
    """
    Test the ImageMedia class when the image url does not exist.

    Returns:
        None
    """
    with pytest.raises(ValueError):
        ImageMedia(url="https://non_existent_url.jpg")


def test_image_media_str_representation(sample_image):
    """
    Test the string representation of the ImageMedia class.

    Args:
        sample_image (ImageMedia): An instance of the ImageMedia class.

    Returns:
        None
    """
    expected_str = f"ImageMedia(url={sample_image.url}, filename={sample_image.filename}), resolution={sample_image.resolution}"
    assert str(sample_image) == expected_str


@pytest.mark.parametrize("width, height", [(100, 200), (300, 400)])
def test_resize_resolution(sample_image, width, height):
    """
    Test the resize_resolution method of the SampleImage class.

    Parameters:
    - sample_image: An instance of the SampleImage class.
    - width: The desired width of the image after resizing.
    - height: The desired height of the image after resizing.

    Returns:
    - None

    Raises:
    - AssertionError: If the resolution of the sample_image does not match
        the specified width and height after resizing.
    """
    sample_image.resize_resolution(width, height)
    assert sample_image.resolution == (width, height)


@pytest.mark.parametrize("scale_factor", [0.5, 2.0])
def test_resize_scale(sample_image, scale_factor):
    """
    Test the resize_scale method of the SampleImage class.

    Parameters:
    - sample_image (SampleImage): The sample image object to be tested.
    - scale_factor (float): The scale factor to resize the image.

    Returns:
    - None

    Raises:
    - AssertionError: If the new resolution does not match the expected value.
    """

    original_resolution = sample_image.resolution
    sample_image.resize_scale(scale_factor)
    new_resolution = sample_image.resolution

    assert new_resolution[0] == int(original_resolution[0] * scale_factor)
    assert new_resolution[1] == int(original_resolution[1] * scale_factor)


@pytest.mark.parametrize("angle", [90, 180, 270])
def test_rotate(sample_image, angle):
    """
    Test the rotate method of the sample_image object.

    Parameters:
    - sample_image: An instance of the SampleImage class.
    - angle: The angle in degrees by which to rotate the image.

    Returns:
    - None

    Raises:
    - AssertionError: If the new resolution of the image after rotation is not equal to the original resolution.
    """

    # Assuming rotation by 90 degrees preserves resolution
    original_resolution = sample_image.resolution
    sample_image.rotate(angle)
    new_resolution = sample_image.resolution

    if angle % 90 == 0:
        assert new_resolution == original_resolution


def test_get_canny(sample_image):
    """
    Test the get_canny method of the sample_image object.

    Parameters:
    - sample_image: An instance of the SampleImage class.

    Returns:
    - None

    Raises:
    - AssertionError: If the result of get_canny is not an instance of np.ndarray.
    """
    # Assuming default values for low_threshold and high_threshold
    canny_result = sample_image.get_canny(50, 150)
    assert isinstance(canny_result, np.ndarray)


def test_get_sobel(sample_image):
    """
    Test the get_sobel() method of the SampleImage class.

    Parameters:
    sample_image (SampleImage): An instance of the SampleImage class.

    Returns:
    None
    """
    sobel_result = sample_image.get_sobel()
    assert isinstance(sobel_result, np.ndarray)
