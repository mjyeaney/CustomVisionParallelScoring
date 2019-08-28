import unittest
import sys
import os
import glob

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from BoundingBoxes import CoordinateOperations

class TestCoordinateOperations(unittest.TestCase):

    def test_coordinate_calcs(self):
        methods = CoordinateOperations()
        x, y = methods.TranslateR4toR2(500, 500, 0, 0, 100, 100)
        self.assertEqual(100, x)
        self.assertEqual(100, y)

        x, y = methods.TranslateR4toR2(500, 500, 1, 0, 100, 100)
        self.assertEqual(600, x)
        self.assertEqual(100, y)

        x, y = methods.TranslateR4toR2(500, 500, 0, 1, 100, 100)
        self.assertEqual(100, x)
        self.assertEqual(600, y)

        x, y = methods.TranslateR4toR2(500, 500, 1, 1, 100, 100)
        self.assertEqual(600, x)
        self.assertEqual(600, y)

        x, y = methods.TranslateR4toR2(500, 500, 3, 1, 100, 100)
        self.assertEqual(1600, x)
        self.assertEqual(600, y)

        x, y = methods.TranslateR4toR2(500, 500, 1, 3, 100, 100)
        self.assertEqual(600, x)
        self.assertEqual(1600, y)
    
    def test_bounding_conditions(self):
        # negatives
        methods = CoordinateOperations()
        with self.assertRaises(Exception):
            x, y = methods.TranslateR4toR2(-500, 500, 1, 5, 100, 100)

        with self.assertRaises(Exception):
            x, y = methods.TranslateR4toR2(500, -500, 1, 5, 100, 100)

        with self.assertRaises(Exception):
            x, y = methods.TranslateR4toR2(500, 500, -1, 5, 100, 100)

        with self.assertRaises(Exception):
            x, y = methods.TranslateR4toR2(500, 500, 1, -5, 100, 100)

        with self.assertRaises(Exception):
            x, y = methods.TranslateR4toR2(500, 500, 1, 5, -100, 100)

        with self.assertRaises(Exception):
            x, y = methods.TranslateR4toR2(500, 500, 1, 5, 100, -100)

if __name__ == '__main__':
    unittest.main()