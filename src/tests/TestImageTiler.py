import unittest
import sys
import os
import glob

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

import ImageTiler

class TestImageTiler(unittest.TestCase):

    def test_tileSize_validation(self):
        tiler = ImageTiler.ImageTiler()
        with self.assertRaises(Exception):
            tiler.WriteTiles("./samples/test-1.jpg", "./samples/tiles", 670, 670, False)
    
    def test_tiling_basics(self):
        tiler = ImageTiler.ImageTiler();
        tiler.WriteTiles("./samples/test-1.jpg", "./samples/tiles", 600, 800, False)
        self.assertEqual(len(glob.glob("./samples/tiles/*.png")), 25)

    def test_tiling_permutations(self):
        tiler = ImageTiler.ImageTiler();
        tiler.WriteTiles("./samples/test-1.jpg", "./samples/tiles", 600, 800, True)
        self.assertEqual(len(glob.glob("./samples/tiles/*.png")), 100)

    def tearDown(self):
        filesToRemove = glob.glob("./samples/tiles/*.png")
        for f in filesToRemove:
            os.remove(f)

if __name__ == '__main__':
    unittest.main()