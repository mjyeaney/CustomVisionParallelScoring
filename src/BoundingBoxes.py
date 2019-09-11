import logging

logger = logging.getLogger("BoundingBoxes")

class CoordinateOperations:
    def RemapBoundingBoxes(self, tileHeight, tileWidth, scores):
        """
        This method re-maps all bounding boxes found to the global space within the original source 
        image.
        """
        # Start with an empty array
        results = []

        # Here, socres is a list of results from our scoring API. 
        for score in scores:
            # Each score contains a list of boxes
            for box in score["boxes"]:
                # Given a tile file name, parse out the name into pieces
                _, index, tileRow, tileCol, angle = score["name"].split('.')[0].split('_')
                x1, y1, x2, y2 = box

                logger.info(f"Mapping box {x1},{y1},{x2},{y2} in row {tileRow}, col {tileCol}...")

                # Translate box coords to R2 using TranslateR4toR2
                x, y = self.TranslateR4toR2(
                    tileWidth, 
                    tileHeight, 
                    int(tileCol), 
                    int(tileRow), 
                    x1, 
                    y1
                )
                width = x2 - x1
                height = y2 - y1

                logger.info(f"New coordinates: {x}, {y} with width = {width} and height = {height}")

                # Add box to output list
                results.append((x, y, x + width, y + height))
        
        return results
    
    def TranslateR4toR2(self, tile_width, tile_height, tile_col, tile_row, r4_x, r4_y):
        """
        This method essentially translates bounding boxes from "tile space" to "source image space". 
        We do this by recognizing that tile space is essentially R4, where each coordinate is not only defined 
        by a _local_ X and Y, but also a tile X and Y (which is row and column). Given a known number of rows and columns, 
        along with tile size, we can perform these translations.
        """

        # Validate range of params is correct
        if (tile_width <= 0): 
            msg = f"Specified tile width {tile_width} cannot be less than / equal to zero";
            logger.error(msg)
            raise Exception(msg)
        
        if (tile_height <= 0): 
            msg = f"Specified tile height {tile_height} cannot be less than / equal to zero";
            logger.error(msg)
            raise Exception(msg)
        
        if (tile_col < 0): 
            msg = f"Specified tile column {tile_col} cannot be less than zero";
            logger.error(msg)
            raise Exception(msg)
        
        if (tile_row < 0): 
            msg = f"Specified tile row {tile_row} cannot be less than zero";
            logger.error(msg)
            raise Exception(msg)

        if (r4_x < 0): 
            msg = f"Specified R4 x value {r4_x} cannot be less than zero";
            logger.error(msg)
            raise Exception(msg)
        
        if (r4_y < 0): 
            msg = f"Specified R4 y value {r4_y} cannot be less than zero";
            logger.error(msg)
            raise Exception(msg)
        
        # Tranlate the coordinate system from R4 to R2
        r2x = (tile_width * tile_col) + r4_x
        r2y = (tile_height * tile_row) + r4_y
        return r2x, r2y