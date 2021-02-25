
from __future__ import annotations

from datetime import datetime
from typing import Iterable, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import shapely

from glacier_lengths.core import iter_geom


def plot_centerlines(centerlines: Union[shapely.geometry.LineString, shapely.geometry.MultiLineString],
                     glacier_outline: Optional[Union[shapely.geometry.Polygon, shapely.geometry.MultiPolygon]] = None,
                     plt_ax: Optional[plt.Axes] = None):

    plt_ax = plt_ax or plt.gca()

    for line in iter_geom(centerlines):
        plt_ax.plot(*line.xy, color="black")

    if glacier_outline is not None:
        for outline in iter_geom(glacier_outline):
            for boundary in iter_geom(glacier_outline.boundary):
                plt_ax.plot(*boundary.xy, color="blue")

    plt_ax.axis("equal")


def plot_length_change(dates: list[Union[datetime.datetime, float]], lengths: list[np.ndarray],
                       plt_ax: Optional[plt.Axes] = None):

    plt_ax = plt_ax or plt.gca()
    assert len(dates) == len(lengths), f"Dates and lengths lists are not the same: {len(dates)} vs {len(lengths)}"

    mean_lengths = [values.mean() for values in lengths]

    plt_ax.plot(dates, mean_lengths, color="black", linestyle="--")

    plt_ax.boxplot(lengths, positions=dates, widths=10)
