import geopandas as gpd

import glacier_lengths
from glacier_lengths import examples

# Read the example data
outlines = gpd.read_file(examples.get_example("rhone-outlines")).sort_values("year")
old_outline = outlines.iloc[0]
new_outline = outlines.iloc[1]
centerline = gpd.read_file(examples.get_example("rhone-centerline")).iloc[0]

# Generate ~40 buffered lines around the glacier centerline
old_buffered_lines = glacier_lengths.buffer_centerline(centerline.geometry, old_outline.geometry)
# Cut the newly generated lines to the new_outline
new_buffered_lines = glacier_lengths.cut_centerlines(old_buffered_lines, new_outline.geometry)

# Measure the lengths of the old and new glacier centerlines.
old_lengths = glacier_lengths.measure_lengths(old_buffered_lines)
new_lengths = glacier_lengths.measure_lengths(new_buffered_lines)

# Print the results.
print(f"""
{old_outline['year']}: {old_lengths.mean():.1f}±{old_lengths.std():.1f} m
{new_outline['year']}: {new_lengths.mean():.1f}±{new_lengths.std():.1f} m
""")
