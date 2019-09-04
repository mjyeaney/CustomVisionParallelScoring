## Data Exchange Patterns

The image processing modules write intermediate files/images to the temporary location defined by the `--tilePath` command line argument. File-based data exchanged was chosen due to the simplicity of debugging, and the ability to have visibility into each step of the processing pipeline.

### Tile File Naming / Encoding

Tile filenames encode the tile position as well as rotation inforamtion in the file name by using the following naming convention:

```
tile_{tile-index}_{tile-row}_{tile-col}_{rotation-angle}.png
```

Each placeholder is described below:

* `tile-index`: The ordinal position of the tile with the segmented source image.
* `tile-row`: The row the current tile belongs to (zero-based).
* `tile-col`: The column within the current row the current tile belongs to (zero-based)
* `rotation-angle`: The angle this tile image has been rotated (one of either 0, 90, 180, 270 degrees).