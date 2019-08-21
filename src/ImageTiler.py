import os, logging
from PIL import Image, ImageFilter

class ImageTiler:
    def writeImageFile(self, image, writePath):
        try:
            logging.info(f"Writing tile: {writePath}")
            image.save(writePath, compress_level=0)
        except:
            logging.error(f"Error while writing {writePath}")
            pass

    def WriteTiles(self, sourceImagePath, outputPath, tileHeight, tileWidth, generatePermutations):
        k = 1
        im = Image.open(sourceImagePath)
        imgwidth, imgheight = im.size
        logging.info(f"Source image info: width={imgwidth}, height={imgheight}, mode={im.mode}")

        for i in range(0, imgheight, tileHeight):
            for j in range(0, imgwidth, tileWidth):
                box = (j, i, j + tileWidth, i + tileHeight)
                
                # Crop image, change colorspace, etc.
                cropped = im.crop(box)
                # cropped = cropped.convert(mode="L") # B&w...does it help?
                # cropped = cropped.filter(ImageFilter.EDGE_ENHANCE) # Edge enhance

                # Write tile images
                writePath = os.path.join(outputPath, f"tile-{k}.png")
                self.writeImageFile(cropped, writePath)            

                # Generate permutations if required
                if generatePermutations:
                    cropped_r90 = cropped.rotate(90, expand=True)
                    cropped_r180 = cropped.rotate(180)
                    writePath = os.path.join(outputPath, f"tile-{k}-r90.png")
                    self.writeImageFile(cropped_r90, writePath)            
                    writePath = os.path.join(outputPath, f"tile-{k}-r180.png")
                    self.writeImageFile(cropped_r180, writePath)

                k +=1
    