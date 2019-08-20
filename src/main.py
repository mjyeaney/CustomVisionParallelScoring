import argparse
import logging
import glob, os
from PIL import Image

LOG_FILE_NAME="log.txt"
LOG_FILE_MODE="w"
LOG_FORMAT="%(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(filename=LOG_FILE_NAME, filemode=LOG_FILE_MODE, format=LOG_FORMAT, level=logging.INFO)

def writeImageFile(image, writePath):
    try:
        logging.info(f"Writing tile at: {writePath}")
        image.save(writePath, compress_level=0)
    except:
        logging.error(f"Error while writing {writePath}")
        pass

def tileSourceImage(sourceImagePath, outputPath, tileHeight, tileWidth):
    k = 1
    im = Image.open(sourceImagePath)
    imgwidth, imgheight = im.size
    logging.info(f"Source image size: width={imgwidth}, height={imgheight}")

    for i in range(0, imgheight, tileHeight):
        for j in range(0, imgwidth, tileWidth):
            box = (j, i, j + tileWidth, i + tileHeight)
            cropped = im.crop(box)
            writePath = os.path.join(outputPath, f"tile-{k}.png")
            writeImageFile(cropped, writePath)

            cropped_r90 = cropped.rotate(90, expand=True)
            writePath = os.path.join(outputPath, f"tile-{k}-r90.png")
            writeImageFile(cropped_r90, writePath)

            cropped_r180 = cropped.rotate(180)
            writePath = os.path.join(outputPath, f"tile-{k}-r180.png")
            writeImageFile(cropped_r180, writePath)

            k +=1

def scoreTiles():
    logging.info("TODO: Invoke API calls to score each tile")

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--tileOnly", help="If present, only tile the image but do not score. Useful for generating training images", action="store_true")
    parser.add_argument("source", help="The path to the source image to create tiles from.", type=str)
    parser.add_argument("targetPath", help="The output path to save the tiles to.", type=str)
    parser.add_argument("tileHeight", help="The height (in pixels) of each output tile", type=int)
    parser.add_argument("tileWidth", help="The width (in pixels) of each output tile", type=int)
    args = parser.parse_args()

    logging.info("Starting tiling utility with the following arguments:")
    logging.info(f"\ttileOnly={args.tileOnly}")
    logging.info(f"\tsource={args.source}")
    logging.info(f"\ttargetPath={args.targetPath}" )
    logging.info(f"\ttileHeight={args.tileHeight}" )
    logging.info(f"\ttileWidth={args.tileWidth}" )

    # 1. Tile the input image
    tileSourceImage(args.source, args.targetPath, args.tileHeight, args.tileWidth)

    # 2. Call the model API endpoint
    #if not args.tileOnly:
        # Let's think through how this may get used from the end-user point of view...
        # Some different decisions here once we get solid model performance
        #scores = scoreTiles()
        #overlayBoundingBoxes(scores)