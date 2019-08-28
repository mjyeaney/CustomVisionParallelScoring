import logging

class CoordinateOperations:
    def CombineBoundingBoxes(self, results):
        # Here, results is a list of results from our Custom Vision API. 
        # For each box found:
             # Translate box coords to R2 using TranslateR4toR2
             # Add box to output list
        
            # Return output list
        pass
    
    def TranslateR4toR2(self, tile_width, tile_height, tile_col, tile_row, r4_x, r4_y):
        # Validate range of params is correct
        if (tile_width < 0): 
            msg = f"Specified tile width {tile_width} cannot be negative";
            logging.error(msg)
            raise Exception(msg)
        
        if (tile_height < 0): 
            msg = f"Specified tile height {tile_height} cannot be negative";
            logging.error(msg)
            raise Exception(msg)
        
        if (tile_col < 0): 
            msg = f"Specified tile column {tile_col} cannot be negative";
            logging.error(msg)
            raise Exception(msg)
        
        if (tile_row < 0): 
            msg = f"Specified tile row {tile_row} cannot be negative";
            logging.error(msg)
            raise Exception(msg)

        if (r4_x < 0): 
            msg = f"Specified R4 x value {r4_x} cannot be negative";
            logging.error(msg)
            raise Exception(msg)
        
        if (r4_y < 0): 
            msg = f"Specified R4 y value {r4_y} cannot be negative";
            logging.error(msg)
            raise Exception(msg)
        
        # Tranlate the coordinate system from R4 to R2
        r2x = (tile_width * tile_col) + r4_x
        r2y = (tile_height * tile_row) + r4_y
        return r2x, r2y