import warnings

import geopandas as gpd
import numpy as np
import pytest
import shapely.geometry

import glacier_lengths
from glacier_lengths import examples


def read_data():
    outlines = gpd.read_file(examples.get_example("rhone-outlines")).sort_values("year")

    old_outline = outlines.iloc[0]
    new_outline = outlines.iloc[1]

    centerline_df = gpd.read_file(examples.get_example("rhone-centerline"))

    centerline = centerline_df.iloc[0]

    assert outlines.crs == centerline_df.crs

    return centerline, old_outline, new_outline


class TestCenterlines:
    centerline, old_outline, new_outline = read_data()

    def test_data(self):
        assert self.centerline.geometry.length > 0
        assert self.old_outline.geometry.area > 0
        assert self.old_outline.geometry.intersects(self.centerline.geometry)

    def test_buffer(self):

        buffered_centrelines = glacier_lengths.buffer_centerline(
            centerline=self.centerline.geometry,
            glacier_outline=self.old_outline.geometry,
            min_radius=5,
            max_radius=50,
            buffer_count=20,
        )
        lengths = [line.length for line in glacier_lengths.core.iter_geom(buffered_centrelines)]

        assert buffered_centrelines.geom_type == "MultiLineString"
        assert len(lengths) > 39
        assert np.std(lengths) < 300

    def test_get_lengths(self):

        buffered_centrelines = glacier_lengths.buffer_centerline(self.centerline.geometry, self.old_outline.geometry)
        lengths = glacier_lengths.measure_lengths(buffered_centrelines)

        assert np.mean(lengths) > 0

    def test_cut(self):

        # Make sure tghat no warnings occur (added because of Shapely deprecation warnings)
        warnings.simplefilter("error")

        buffered_centrelines = glacier_lengths.buffer_centerline(self.centerline.geometry, self.old_outline.geometry)

        cut_centerlines = glacier_lengths.cut_centerlines(buffered_centrelines, self.new_outline.geometry)

        cut_lines = self.new_outline.geometry.boundary
        if cut_lines.geom_type == "MultiLineString":
            # Extract the longest line.
            cut_line = sorted(cut_lines.geoms, key=lambda x: x.length)[-1]
        else:
            cut_line = cut_lines

        cut_centerlines2 = glacier_lengths.cut_centerlines(buffered_centrelines, cut_line)

        old_lengths = glacier_lengths.measure_lengths(buffered_centrelines)
        new_lengths = glacier_lengths.measure_lengths(cut_centerlines)
        new_lengths2 = glacier_lengths.measure_lengths(cut_centerlines2)

        # Verify that warnings are triggered with a weird cutting geometry
        with pytest.warns(match="Centerline nr. .* was not cut by the cutting geometry."):
            glacier_lengths.cut_centerlines(buffered_centrelines, shapely.geometry.LineString([(0, 0), (1, 1)]))

        # (Implicitly) verify that no warning is triggered with a weird cutting geometry if explicitly requested
        glacier_lengths.cut_centerlines(
            buffered_centrelines, shapely.geometry.LineString([(0, 0), (1, 1)]), warn_if_not_cut=False
        )

        assert old_lengths.mean() > new_lengths.mean()
        assert abs(new_lengths.mean() - new_lengths2.mean()) < 0.01

        # Test that the distance threshold changes the count of valid centerlines
        all_lines = glacier_lengths.cut_centerlines(buffered_centrelines, cut_line, max_difference_fraction=1)
        conservative_lines = glacier_lengths.cut_centerlines(
            buffered_centrelines, cut_line, max_difference_fraction=1e-3
        )

        assert len(all_lines.geoms) > len(conservative_lines.geoms)

    @pytest.mark.skip("Not a quantitative test. Should be excluded in test suite.")
    def test_temp_plotting(self):

        import matplotlib.pyplot as plt

        from glacier_lengths.plotting import plot_centerlines

        buffered_centrelines = glacier_lengths.buffer_centerline(self.centerline.geometry, self.old_outline.geometry)

        cut_centerlines = glacier_lengths.cut_centerlines(buffered_centrelines, self.new_outline.geometry)

        plt.subplot(121)
        plot_centerlines(buffered_centrelines, self.old_outline.geometry)
        plt.subplot(122)
        plot_centerlines(cut_centerlines, self.new_outline.geometry)

        plt.show()
