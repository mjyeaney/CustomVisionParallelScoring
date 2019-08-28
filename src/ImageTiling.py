import os, logging
from PIL import Image, ImageFilter

class DefaultImageTiler:
    def __writeImageFile(self, image, writePath):
        try:
            logging.info(f"Writing tile: {writePath}")
            image.save(writePath, compress_level=0)
        except:
            logging.error(f"Error while writing {writePath}")
            pass
    
    def __validateTileSize(self, sourceHeight, tileHeight, sourceWidth, tileWidth):
        if (sourceHeight % tileHeight != 0):
            msg = f"Specified tile height {tileHeight} does not evenly divide source image {sourceHeight}.";
            logging.error(msg)
            raise Exception(msg)
        
        if (sourceWidth % tileWidth != 0):
            msg = f"Specified tile width {tileWidth} does not evenly divide source image {sourceWidth}.";
            logging.error(msg)
            raise Exception(msg)

    def WriteTiles(self, sourceImagePath, outputPath, tileHeight, tileWidth, generatePermutations):
        """
        Breaks a source image into smaller tiles, defined by the h/w passed in by caller. Tiles are written to an
        intermediate location on disk storage, and used later by other modules.
        """

        k = 1
        im = Image.open(sourceImagePath)
        imgwidth, imgheight = im.size
        logging.info(f"Source image info: width={imgwidth}, height={imgheight}, mode={im.mode}")

        # Validate that stil size evenly divides source image
        self.__validateTileSize(imgheight, tileHeight, imgwidth, tileWidth)

        # Create tiles
        for i in range(0, imgheight, tileHeight):
            for j in range(0, imgwidth, tileWidth):
                box = (j, i, j + tileWidth, i + tileHeight)
                
                # Crop image, change colorspace, etc.
                cropped = im.crop(box)

                # Few other options to test: B&W and Edge enhanced
                # cropped = cropped.convert(mode="L") # B&w...does it help?
                # cropped = cropped.filter(ImageFilter.EDGE_ENHANCE) # Edge enhance

                # Write tile images
                writePath = os.path.join(outputPath, f"tile_{k}.png")
                self.__writeImageFile(cropped, writePath)            

                # Generate permutations if required (3 per original image, yielding 4 samples per tile)
                if generatePermutations:
                    cropped_r90 = cropped.rotate(90, expand=True)
                    cropped_r180 = cropped.rotate(180)
                    cropped_r270 = cropped.rotate(270, expand=True)

                    writePath = os.path.join(outputPath, f"tile_{k}_r90.png")
                    self.__writeImageFile(cropped_r90, writePath)
                    writePath = os.path.join(outputPath, f"tile_{k}_r180.png")
                    self.__writeImageFile(cropped_r180, writePath)
                    writePath = os.path.join(outputPath, f"tile_{k}_r270.png")
                    self.__writeImageFile(cropped_r270, writePath)
                
                # Increment tile counter
                k +=1
    