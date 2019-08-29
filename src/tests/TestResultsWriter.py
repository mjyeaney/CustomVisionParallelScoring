import unittest
import sys
import os
import glob

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from ResultsWriter import ImageWithBoundingBoxes

class TestResultsWriter(unittest.TestCase):

    def test_basic_box_drawing(self):
        writer = ImageWithBoundingBoxes()
        boxes = []
        boxes.append((500, 500, 700, 700))
        writer.Write("./samples/test-1.jpg", boxes, "./samples/results/test-1-results.jpg")
    
    def test_multiple_box_drawing(self):
        writer = ImageWithBoundingBoxes()
        boxes = []
        boxes.append((500, 500, 700, 700))
        boxes.append((800, 500, 1000, 700))
        boxes.append((900, 900, 1100, 1100))
        boxes.append((1200, 900, 1400, 1100))
        writer.Write("./samples/test-1.jpg", boxes, "./samples/results/test-2-results.jpg")

    def tearDown(self):
        filesToRemove = glob.glob("./samples/results/*.jpg")
        for f in filesToRemove:
            os.remove(f)

if __name__ == "__main__":
    unittest.main()