import unittest
import sys
import os
import glob

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from ImageTiling import DefaultImageTiler

class TestImageTiler(unittest.TestCase):

    def test_tileSize_validation(self):
        tiler = DefaultImageTiler("./samples/tiles", 670, 670)
        with self.assertRaises(Exception):
            tiler.CreateTiles("./samples/test-1.jpg", False)
    
    def test_tiling_basics(self):
        tiler = DefaultImageTiler("./samples/tiles", 600, 800);
        tiler.CreateTiles("./samples/test-1.jpg", False)
        self.assertEqual(len(glob.glob("./samples/tiles/*.png")), 25)

    def test_tiling_permutations(self):
        tiler = DefaultImageTiler("./samples/tiles", 600, 800);
        tiler.CreateTiles("./samples/test-1.jpg", True)
        self.assertEqual(len(glob.glob("./samples/tiles/*.png")), 100)

    def tearDown(self):
        filesToRemove = glob.glob("./samples/tiles/*.png")
        for f in filesToRemove:
            os.remove(f)

if __name__ == '__main__':
    unittest.main()