# Plot Colorschemes

## Comparison

| | PCA plot (`interactive_3d.html`) | Correlation plots (`distance_plot`) |
|---|---|---|
| **Colour value** | Ontological distance from the first concept (`D_snomed[0]`) — a relational metric | `ancestor_count` — intrinsic property of each concept (depth in IS-A hierarchy) |
| **Colormap** | Viridis (string passed to Plotly) | Viridis (applied manually via `plt.cm.viridis` + `mcolors.to_hex`) |
| **Library** | Plotly (`interactive_3d_plot` in `utils.py`) | Matplotlib (`distance_plot` in `utils.py`) |
| **When computed** | At plot time, directly from `D_snomed` | Requires `ancestor_count` persisted in `concepts.csv` through the pipeline |

## Key Difference

Both use Viridis, but they colour by different things:

- The **PCA plot** already had meaningful colouring from the start — each point's colour shows
  how ontologically far that concept is from the first concept in the dataset.
- The **correlation plots** previously used the arbitrary point index `i` as the colour value.
  They were updated to use `ancestor_count` (number of IS-A ancestors in SNOMED CT), which is
  an intrinsic measure of how deep each concept sits in the hierarchy. This required adding
  `ancestor_count` as a column in `concepts.csv` (notebook 1) so it is available in notebook 3.
