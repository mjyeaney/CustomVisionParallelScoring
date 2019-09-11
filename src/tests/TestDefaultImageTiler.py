import unittest
import sys
import os
import glob

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from Settings import ConfigSettings
from ImageTiling import DefaultImageTiler

class TestImageTiler(unittest.TestCase):

    def test_tileSize_validation(self):
        config = ConfigSettings()
        config.tempFilePath = "./samples/tempFiles"
        tiler = DefaultImageTiler(config, 670, 670)
        with self.assertRaises(Exception):
            tiler.CreateTiles("./samples/test-1.jpg", False)
    
    def test_tiling_basics(self):
        config = ConfigSettings()
        config.tempFilePath = "./samples/tempFiles"
        tiler = DefaultImageTiler(config, 600, 800);
        tiler.CreateTiles("./samples/test-1.jpg", False)
        self.assertEqual(len(glob.glob("./samples/tempFiles/*.png")), 25)
        tiler.Cleanup()

    def test_tiling_permutations(self):
        config = ConfigSettings()
        config.tempFilePath = "./samples/tempFiles"
        tiler = DefaultImageTiler(config, 600, 800);
        tiler.CreateTiles("./samples/test-1.jpg", True)
        self.assertEqual(len(glob.glob("./samples/tempFiles/*.png")), 100)
        tiler.Cleanup()


if __name__ == '__main__':
    unittest.main()