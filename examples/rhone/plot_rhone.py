import geopandas as gpd
import matplotlib.pyplot as plt

import glacier_lengths
import glacier_lengths.plotting


def plot_rhone():
    outlines = gpd.read_file("examples/rhone/data/outlines.shp").sort_values("year")
    outlines["year"] = outlines["year"].astype(int)

    old_outline = outlines.iloc[0]
    new_outline = outlines.iloc[1]

    centerline = gpd.read_file("examples/rhone/data/centerline.shp").iloc[0]

    old_buffered_lines = glacier_lengths.buffer_centerline(centerline.geometry, old_outline.geometry)
    new_buffered_lines = glacier_lengths.cut_centerlines(old_buffered_lines, new_outline.geometry)

    old_lengths = glacier_lengths.measure_lengths(old_buffered_lines)
    new_lengths = glacier_lengths.measure_lengths(new_buffered_lines)
    print(f"""
    {old_outline['year']}: {old_lengths.mean():.1f}±{old_lengths.std():.1f} m
    {new_outline['year']}: {new_lengths.mean():.1f}±{new_lengths.std():.1f} m
    """)

    plt.figure(figsize=(12, 5))
    plt.subplot(131)
    plt.title(f"Glacier {old_outline.year}")
    glacier_lengths.plotting.plot_centerlines(old_buffered_lines, old_outline.geometry)
    old_xlim = plt.gca().get_xlim()
    old_ylim = plt.gca().get_ylim()
    plt.yticks(rotation=45, va="center")
    plt.subplot(132)
    plt.title(f"Glacier {new_outline.year}")
    glacier_lengths.plotting.plot_centerlines(new_buffered_lines, new_outline.geometry)
    plt.xlim(old_xlim)
    plt.ylim(old_ylim)
    plt.yticks(rotation=45, va="center")
    plt.subplot(133)
    plt.title(f"Length change {old_outline.year}–{new_outline.year}")
    glacier_lengths.plotting.plot_length_change(
        [old_outline["year"], new_outline["year"]],
        [old_lengths / 1000, new_lengths / 1000]
    )
    plt.ylabel("Length (km)")
    plt.ylim(9, 12)
    plt.xlim(1900, 2040)
    plt.tight_layout()

    plt.savefig("examples/rhone/rhone.jpg", dpi=300)
    plt.show()


if __name__ == "__main__":
    plot_rhone()
