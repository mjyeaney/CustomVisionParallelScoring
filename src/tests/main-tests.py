import unittest
import sys
import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

import main

if __name__ == "__main__":
    main.scoreTiles()