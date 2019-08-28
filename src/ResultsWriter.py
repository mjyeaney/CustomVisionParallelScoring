import logging
from PIL import Image

class ImageWithBoundingBoxes:
    def Write(self, originalSource, boundingBoxes):
        # Use PIL.ImageDraw.ImageDraw.rectangle(xy, fill=None, outline=None, width=0) to overlay boxes
        pass