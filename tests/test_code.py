"""Test code standards."""


import os

import pylint.epylint

import glacier_lengths


def test_pylint():

    output_text = pylint.epylint.py_run(os.path.dirname(glacier_lengths.__file__), return_std=True)[0].read()

    start_pattern = "has been rated at"
    end_pattern = "/10"
    score = output_text[output_text.index(start_pattern) + len(start_pattern):]
    score = float(score[:score.index(end_pattern)])

    assert score > 0.95
