"""Auxiliary plotting functions."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import shapely

from glacier_lengths.core import iter_geom


def plot_centerlines(centerlines: Union[shapely.geometry.LineString, shapely.geometry.MultiLineString],
                     glacier_outline: Optional[Union[shapely.geometry.Polygon, shapely.geometry.MultiPolygon]] = None,
                     plt_ax: Optional[plt.Axes] = None,
                     centerline_kwargs: dict[str, Any] = None,
                     outline_kwargs: dict[str, Any] = None) -> None:
    """
    Plot glacier centerlines.

    `plt.show()` or similar has to be run to display the figure.

    :param centerlines: One or multiple glacier centrelines.
    :param glacier_outline: Optional. Glacier outline to give the centerlines context.
    :param plt_ax: Optional. A matplotlib axis to draw on. Defaults to the current axis.
    :param centerline_kwargs: Optional. Keyword arguments to supply the centerline matplotlib plot() call.
    :param outline_kwargs: Optional. Keyword arguments to supply the outline matplotlib plot() call.
    """
    if centerline_kwargs is None:
        centerline_kwargs = {}
    if outline_kwargs is None:
        outline_kwargs = {}
    if "color" not in centerline_kwargs:
        centerline_kwargs["color"] = "blue"
    if "color" not in outline_kwargs:
        outline_kwargs["color"] = "black"

    plt_ax = plt_ax or plt.gca()

    for line in iter_geom(centerlines):
        plt_ax.plot(*line.xy, **centerline_kwargs)

    if glacier_outline is not None:
        for outline in iter_geom(glacier_outline):
            for boundary in iter_geom(outline.boundary):
                plt_ax.plot(*boundary.xy, **outline_kwargs)

    plt_ax.axis("equal")


def plot_length_change(dates: list[Union[datetime, float]], lengths: list[np.ndarray],
                       plt_ax: Optional[plt.Axes] = None) -> None:
    """
    Plot length change as boxplots with associated errors.

    len(dates) have to be equal to len(lengths)

    :param dates: The dates of the length measurements.
    :param lengths: A list of length measurements (one array per date).
    :param plt_ax: Optional. A matplotlib axis to draw on. Defaults to the current axis.
    """
    plt_ax = plt_ax or plt.gca()
    assert len(dates) == len(lengths), f"Dates and lengths lists are not the same: {len(dates)} vs {len(lengths)}"

    mean_lengths = [values.mean() for values in lengths]

    plt_ax.plot(dates, mean_lengths, color="black", linestyle="--")

    plt_ax.boxplot(lengths, positions=dates, widths=10)
