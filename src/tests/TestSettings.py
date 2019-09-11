import unittest
import sys
import os
import glob

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from Settings import ConfigSettings

class TestSettings(unittest.TestCase):
    """
    Tests the default settings class behavior.
    """

    def test_handling_missing_filename(self):
        config = ConfigSettings()
        self.assertEqual(config.tempFilePath, None)
        self.assertEqual(config.serviceEndpoint, None)
        self.assertEqual(config.publishIterationName, None)
        self.assertEqual(config.projectId, None)
        self.assertEqual(config.predictionResourceId, None)
        self.assertEqual(config.predictionKey, None)
        self.assertEqual(config.boundingBoxScoreThreshold, 0.0)
    
    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            config = ConfigSettings("file-that-doesn-exist.cfg")

