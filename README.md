## glacier\_lengths — Statistical glacier length calculations

[![build](https://github.com/erikmannerfelt/glacier_lengths/actions/workflows/python-package.yml/badge.svg)](https://github.com/erikmannerfelt/glacier_lengths/actions/workflows/python-package.yml)
[![pypi](https://github.com/erikmannerfelt/glacier_lengths/actions/workflows/python-publish.yml/badge.svg)](https://github.com/erikmannerfelt/glacier_lengths/actions/workflows/python-publish.yml)

[![PyPI version fury.io](https://badge.fury.io/py/glacier-lengths.svg)](https://pypi.python.org/pypi/glacier-lengths/)

Often when glacier lengths are calculated, only the glacier centerline is considered.
This is arguably not a statistically representative measure for the entire front, as it just considers one point on the glacier outline.
The `glacier_lengths` package aims to simplify length calculations along an arbitrary amount of lines buffered around the glacier centerline.

### Installation
`pip install glacier_lengths` (will soon work)

`pip install git+https://github.com/erikmannerfelt/glacier_lengths.git`

### Example
Calculate the length change of Rhonegletscher:
```python
import geopandas as gpd
import glacier_lengths

# Read the example data
outlines = gpd.read_file("examples/rhone/data/outlines.shp").sort_values("year")
old_outline = outlines.iloc[0]
new_outline = outlines.iloc[1]
centerline = gpd.read_file("examples/rhone/data/centerline.shp").iloc[0]

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
```
prints:
```bash
1928: 10783.6±38.8 m
2020: 9699.9±7.6 m
```

#### Plot a figure
```bash
python examples/rhone/plot_rhone.py
```
![](https://i.imgur.com/vCyrYlE.jpg)

### Testing
Run `python -m pytest` in the cloned repo base directory.
