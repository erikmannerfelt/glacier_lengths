from __future__ import annotations

from typing import Any, Iterable, Union

import numpy as np
import shapely


def extrapolate_point(point_1: tuple[float, float], point_2: tuple[float, float]) -> tuple[float, float]:
    """Create a point extrapoled in p1->p2 direction."""
    # p1 = [p1.x, p1.y]
    # p2 = [p2.x, p2.y]
    extrap_ratio = 10
    return (point_1[0]+extrap_ratio*(point_2[0]-point_1[0]), point_1[1]+extrap_ratio*(point_2[1]-point_1[1]))


def iter_geom(geometry) -> Iterable:
    """
    Return an iterable of the geometry.

    Example: 'geometry' is either a LineString or a MultiLineString. Only MultiLineString can be iterated over normally.
    """
    if "Multi" in geometry.geom_type or geometry.geom_type == "GeometryCollection":
        return geometry

    return [geometry]


def type_check_single_line(geometry: Any, variable_name: str) -> None:
    """Check if the given object is a shapely.geometry.LineString."""
    try:
        if geometry.geom_type == "LineString":
            return
    except AttributeError:
        pass

    raise TypeError(f"{variable_name} had incorrect type: {type(geometry)}, expected: 'LineString'")


def type_check_line(geometry: Any, variable_name: str) -> None:
    """
    Check if the given object is either a shapely.geometry.LineString or a MultiLineString.

    :raises TypeError: If the type is not a line.
    """
    try:
        if geometry.geom_type in ["LineString", "MultiLineString"]:
            return
    except AttributeError:
        pass

    raise TypeError(f"{variable_name} had incorrect type: {type(geometry)},"
                    " expected one of: ['LineString', 'MultiLineString']")


def type_check_polygon(geometry: Any, variable_name: str) -> None:
    """Check if the given object is either a shapely.geometry.Polygon or a MultiPolygon."""
    try:
        if geometry.geom_type in ["Polygon", "MultiPolygon"]:
            return
    except AttributeError:
        pass

    raise TypeError(f"{variable_name} had incorrect type: {type(geometry)},"
                    " expected one of: ['Polygon', 'MultiPolygon']")


def type_check_single_line_or_polygon(geometry: Any, variable_name: str) -> None:
    """Check if the given object is either a shapely.geometry.Polygon, a MultiPolygon or a LineString."""
    try:
        if geometry.geom_type in ["Polygon", "MultiPolygon", "LineString"]:
            return
    except AttributeError:
        pass

    raise TypeError(f"{variable_name} had incorrect type: {type(geometry)},"
                    " expected one of: ['Polygon', 'MultiPolygon', 'LineString']")


def buffer_centerline(centerline: shapely.geometry.LineString, glacier_outline: shapely.geometry.MultiPolygon,
                      min_radius: float = 1.0, max_radius: float = 50, buffer_count: int = 20):
    """
    Return buffered glacier centerlines (lines parallel to the centerline).

    Note that the centerline coordinates should be ordered from glacier start to glacier end.

    :param centerline: The glacier centerline.
    :param glacier_outline: The glacier outline polygon.
    :param min_radius: The minimum buffer radius in georeferenced units.
    :param max_radius: The maximum buffer radius in georeferenced units.
    :param buffer_count: The amount of buffers to create. Will return approximately twice the count (one for each side).

    :returns: Multiple buffered glacier centerlines.
    """
    # Make sure the inputs have correct types.
    type_check_single_line(centerline, "centerline")
    type_check_polygon(glacier_outline, "glacier_outline")

    assert centerline.intersects(glacier_outline), "centerline does not intersect the glacier_outline!"

    # The maximum allowed line distance from the initial centreline point
    # This is to make sure that all lines have an almost common starting point (eg instead of being cropped mid-glacier)
    distance_threshold = max(centerline.length * 0.1, max_radius * (2 ** 0.5))

    # Extrapolate the centerline back and forth to ensure that it will cut the glacier edges.
    coords = list(centerline.coords)
    coords.insert(0, extrapolate_point(coords[1], coords[0]))
    coords.insert(-1, extrapolate_point(coords[-2], coords[-1]))
    cropped_full_centerline = shapely.geometry.LineString(coords).intersection(glacier_outline)
    full_centerline = sorted((line for line in iter_geom(cropped_full_centerline)), key=lambda line: line.length)[-1]
    full_centerline_coords = list(full_centerline.coords)
    full_centerline_coords.insert(-1, extrapolate_point(full_centerline_coords[-2], full_centerline_coords[-1]))
    extended_centreline = shapely.geometry.LineString(full_centerline_coords)

    # Initialise a list of LineStrings
    buffered_centerlines: list[shapely.geometry.LineString] = []

    # Loop over each buffer distance and make a buffer from it.
    for buffer in np.linspace(min_radius, max_radius, num=buffer_count):
        # Buffer the line and extract the LineString outline (boundary)
        buffered = extended_centreline.buffer(buffer).boundary

        # Extract only the parts of the lines that intersect (lie within) the glacier outline
        intersection = buffered.intersection(glacier_outline)

        # Loop over each line, and merge ones that touch each other.
        merged_lines: list[shapely.geometry.LineString] = []
        for line in iter_geom(intersection):
            touching = False
            # Loop through all lines in the lines_inside list and merge touching lines
            for i, line2 in enumerate(merged_lines):
                if line2.touches(line):
                    merged_lines[i] = shapely.ops.linemerge([line, line2])
                    touching = True
                    break
            # If it doesn't touch any line, add it to the lines list
            if not touching:
                merged_lines.append(line)

        # Loop over all merged lines and try to figure out if it is a representative centerline
        for line in merged_lines:
            # Extract the first and last point coordinates of the line
            first_and_last_points = np.array([
                [line.xy[0][0], line.xy[1][0]],
                [line.xy[0][-1], line.xy[1][-1]]
            ])
            # Check the distance between the first/last point to the first point of the centerline.
            distances = np.linalg.norm(
                first_and_last_points - np.array([centerline.xy[0][0], centerline.xy[1][0]]),
                axis=1)

            # Skip if neither the beginning nor the end of the line is close to the beginning of the centerline
            if np.count_nonzero(distances < distance_threshold) == 0:
                continue

            # If the line's length is less than 60% of the centerline's, it's probably invalid
            if (line.length / centerline.length) < 0.6:
                continue

            # Revert the line if it starts at the bottom and ends at the top (all should start at the top)
            if distances[1] > distances[0]:  # Checks if the end point is closer than the start point
                line = shapely.geometry.LineString(list(line.coords)[::-1])

            # If the line has come here, it is assumed to be a valid buffered centerline
            buffered_centerlines.append(line)

    # Return a merged version of the buffered centerlines
    merged_geometry = shapely.ops.linemerge(buffered_centerlines)
    assert not merged_geometry.is_empty, "Buffer failed. Output geometry is empty"
    assert merged_geometry.geom_type == "MultiLineString", f"Buffer had incorrect output: {type(merged_geometry)}"\
        ", expected 'MultiLineString'"
    return merged_geometry


def geometry_to_line(geometry) -> Union[shapely.geometry.LineString, shapely.geometry.MultiLineString]:
    if geometry.geom_type in ["LineString", "MultiLineString"]:
        return geometry

    if geometry.geom_type in ["Polygon", "MultiPolygon"]:
        exteriors = [shapely.geometry.LineString(geom.exterior.coords) for geom in iter_geom(geometry)]
        exterior = shapely.ops.linemerge(exteriors)

        return exterior


def cut_centerlines(centerlines: Union[shapely.geometry.LineString, shapely.geometry.MultiLineString],
                    cutting_geometry: Union[shapely.geometry.LineString,
                                            shapely.geometry.Polygon, shapely.geometry.MultiPolygon]
                    ) -> Union[shapely.geometry.LineString, shapely.geometry.MultiLineString]:
    """
    Cut glacier centerlines with another geometry.

    The other geometry could be a glacier outline or a glacier front line.

    :param centerlines: One or multiple glacier centerlines.
    :param cutting_geometry: A supported geometry to cut the centerlines with.

    :returns: Cut glacier centerlines.
    """
    type_check_line(centerlines, "centerlines")
    type_check_single_line_or_polygon(cutting_geometry, "cutting_geometry")

    # Find the longest centerline and use it as a proxy for the actual centerline.
    longest_centerline = centerlines if centerlines.geom_type == "LineString" else centerlines[0]
    if centerlines.geom_type != "LineString":
        for line in centerlines:
            if line.length > longest_centerline.length:
                longest_centerline = line
    # The maximum allowed line distance from the initial centreline point
    # This is to make sure that all lines have an almost common starting point (eg instead of being cropped mid-glacier)
    distance_threshold = longest_centerline.length * 0.2
    cutter = geometry_to_line(cutting_geometry)
    cut_geometry = shapely.ops.split(centerlines, cutter)

    assert cut_geometry.length > 0

    cropped_centrelines: list[shapely.geometry.LineString] = []
    for line in iter_geom(cut_geometry):
        first_and_last_points = np.array([
            [line.xy[0][0], line.xy[1][0]],
            [line.xy[0][-1], line.xy[1][-1]]
        ])
        distances = np.linalg.norm(
            first_and_last_points - np.array([longest_centerline.xy[0][0], longest_centerline.xy[1][0]]),
            axis=1)
        if np.count_nonzero(distances < distance_threshold) == 0:
            continue

        if (line.length / longest_centerline.length) < 0.2:
            continue
        cropped_centrelines.append(line)

    merged_lines = shapely.ops.linemerge(cropped_centrelines)

    assert not merged_lines.is_empty, f"Centerline cutting failed: empty geometry"

    return merged_lines


def measure_lengths(centerlines: Union[shapely.geometry.LineString, shapely.geometry.MultiLineString]) -> np.ndarray:
    """
    Measure the lengths of the given glacier centerlines.

    :param centerlines: One or multiple glacier centerlines.

    :returns: An array of lengths with shape (N,) where N is the amount of centerlines.
    """
    lengths = np.array([line.length for line in iter_geom(centerlines)])

    return lengths
