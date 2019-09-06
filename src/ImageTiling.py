import os, glob, logging
from PIL import Image, ImageFilter

class DefaultImageTiler:
    """
    Basic image tiling support. Breaks down the source image into a number of tiles each of which 
    has a defined size. Tiles MUST evenly divide the width and height of the source image.
    """

    def __init__(self, tilePath, tileHeight, tileWidth):
        self.tilePath = tilePath
        self.tileHeight = tileHeight
        self.tileWidth = tileWidth

    def __writeImageFile(self, image, writePath):
        try:
            logging.info(f"Writing tile: {writePath}")
            image.save(writePath, compress_level=0)
        except:
            logging.error(f"Error while writing {writePath}")
            pass
    
    def __validateTileSize(self, sourceHeight, sourceWidth):
        if (sourceHeight % self.tileHeight != 0):
            msg = f"Specified tile height {self.tileHeight} does not evenly divide source image {sourceHeight}.";
            logging.error(msg)
            raise Exception(msg)
        
        if (sourceWidth % self.tileWidth != 0):
            msg = f"Specified tile width {self.tileWidth} does not evenly divide source image {sourceWidth}.";
            logging.error(msg)
            raise Exception(msg)
    
    def Cleanup(self):
        """
        Cleans up temporary tile images that were created.
        """
        logging.info("Removing tiles...")
        filesToRemove = glob.glob(os.path.join(self.tilePath, "*.png"))
        logging.info(f"Found {len(filesToRemove)} tiles...")
        for f in filesToRemove:
            os.remove(f)

    def CreateTiles(self, sourceImagePath, generatePermutations):
        """
        Breaks a source image into smaller tiles, defined by the h/w passed in by caller. Tiles are written to an
        intermediate location on disk storage, and used later by other modules.
        """

        k = 1
        tileRow = 0
        tileCol = 0
        im = Image.open(sourceImagePath)
        imgwidth, imgheight = im.size
        logging.info(f"Source image info: width={imgwidth}, height={imgheight}, mode={im.mode}")

        # Validate that stil size evenly divides source image
        self.__validateTileSize(imgheight, imgwidth)

        # Create tiles
        for i in range(0, imgheight, self.tileHeight):
            for j in range(0, imgwidth, self.tileWidth):
                box = (j, i, j + self.tileWidth, i + self.tileHeight)
                
                # Crop image, change colorspace, etc.
                cropped = im.crop(box)

                # Few other options to test: B&W and Edge enhanced
                # cropped = cropped.convert(mode="L") # B&w...does it help?
                # cropped = cropped.filter(ImageFilter.EDGE_ENHANCE) # Edge enhance

                # Write tile images - note we're encoding tiling infomration into the filenames
                writePath = os.path.join(self.tilePath, f"tile_{k}_{tileRow}_{tileCol}_0.png")
                self.__writeImageFile(cropped, writePath)            

                # Generate permutations if required (3 per original image, yielding 4 samples per tile)
                if generatePermutations:
                    cropped_r90 = cropped.rotate(90, expand=True)
                    cropped_r180 = cropped.rotate(180)
                    cropped_r270 = cropped.rotate(270, expand=True)

                    writePath = os.path.join(self.tilePath, f"tile_{k}_{tileRow}_{tileCol}_90.png")
                    self.__writeImageFile(cropped_r90, writePath)
                    writePath = os.path.join(self.tilePath, f"tile_{k}_{tileRow}_{tileCol}_180.png")
                    self.__writeImageFile(cropped_r180, writePath)
                    writePath = os.path.join(self.tilePath, f"tile_{k}_{tileRow}_{tileCol}_270.png")
                    self.__writeImageFile(cropped_r270, writePath)
                
                # Increment counters
                k +=1
                tileCol += 1
            
            tileCol = 0
            tileRow += 1
    