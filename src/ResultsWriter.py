import logging
from PIL import Image, ImageDraw

logger = logging.getLogger("ResultsWriter")

class ImageWithBoundingBoxes:
    """
    Draws a final image with boxes overlayed on it.
    """
    COLOR = "#ffff00"
    BORDER_WIDTH = 4

    def Write(self, originalSource, boundingBoxes, outputPath):
        """
        Writes the final image using the bounding boxes defined in the boundingBoxes paramters. 
        Bounding boxes are an array, with each element being a 4-tuple containing (x1, y1, x2, y2).
        """

        logger.info("Creating results image with overlays...")

        # Open the image and create 2D drawing context
        im = Image.open(originalSource)
        draw = ImageDraw.Draw(im)

        # Iterate the boxes that were given
        logger.info("- Drawing bounding boxes")
        for box in boundingBoxes:
            draw.rectangle(box, fill=None, outline=self.COLOR, width=self.BORDER_WIDTH)

        # Close the drawing context and write the image
        del draw
        im.save(outputPath, "JPEG")
        logger.info("Done!!")