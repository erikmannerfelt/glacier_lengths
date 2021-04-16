"""Example data auxiliary functions."""
import os
import shutil
import tarfile
import tempfile
import urllib.request
from glob import glob

import glacier_lengths

EXAMPLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../examples/")

EXAMPLE_FILES = {
    "rhone-outlines": os.path.join(EXAMPLES_DIR, "rhone/data/outlines.shp"),
    "rhone-centerline": os.path.join(EXAMPLES_DIR, "rhone/data/centerline.shp")
}

TEMP_DIR = tempfile.TemporaryDirectory()


def download_examples(overwrite: bool = False) -> str:
    """
    Download examples from the GitHub repo to a temporary directory.

    :param overwrite: Overwrite the files even though they exist?

    :raises ValueError: If the data could not be fetched from the GitHub repo.

    :returns: A filepath to the temporary directory.
    """
    # The URL from which to download the repository
    url = "https://github.com/erikmannerfelt/glacier_lengths/tarball/main"

    tar_path = os.path.join(TEMP_DIR.name, "data.tar.gz")

    # Download the tarball if it doesn't already exist
    if not overwrite and not os.path.isfile(tar_path):
        print("Downloading latest examples...")

        response = urllib.request.urlopen(url)
        # If the response was right, download the tarball to the temporary directory
        if response.getcode() == 200:
            with open(tar_path, "wb") as outfile:
                outfile.write(response.read())
        else:
            raise ValueError(f"Example data fetch gave non-200 response: {response.status_code}")

        # Extract the tarball
        with tarfile.open(tar_path) as tar:
            tar.extractall(TEMP_DIR.name)

    return glob(TEMP_DIR.name + "/*/examples/")[0]


def get_example(name: str):
    """
    Retrieve the path to an example file.

    Files will be downloaded from GitHub if they cannot be found.

    :returns: An absolute filepath to the given example.
    """
    if not os.path.isfile(EXAMPLE_FILES[name]):
        examples_dir = download_examples(overwrite=False)
        return EXAMPLE_FILES[name].replace(EXAMPLES_DIR, examples_dir)

    return EXAMPLE_FILES[name]
