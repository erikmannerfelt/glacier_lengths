"""Example data auxiliary functions."""
import os

EXAMPLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../examples/")

EXAMPLE_FILES = {
    "rhone-outlines": os.path.join(EXAMPLES_DIR, "rhone/data/outlines.shp"),
    "rhone-centerline": os.path.join(EXAMPLES_DIR, "rhone/data/centerline.shp")
}


def get_example(name: str):
    """Retrieve the path to an example file.

    :returns: An absolute filepath to the given example.
    """
    return EXAMPLE_FILES[name]
