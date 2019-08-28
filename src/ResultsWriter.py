import logging
from PIL import Image

class ImageWithBoundingBoxes:
    def Write(self, originalSource, boundingBoxes, outputPath):
        # Use PIL.ImageDraw.ImageDraw.rectangle(xy, fill=None, outline=None, width=0) to overlay boxes
        # Assume that boundingBoxes is an array of tuples containing (x1, y1, h, w)
        pass