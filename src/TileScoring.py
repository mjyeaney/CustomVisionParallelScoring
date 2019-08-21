import logging, os
import glob

class TileScoring:
    def ScoreTiles(self, tileDirectory):
        tiles = glob.glob(os.path.join(tileDirectory, "*.png"))
        logging.info(f"Found {len(tiles)} tiles for scoring (TODO)...")