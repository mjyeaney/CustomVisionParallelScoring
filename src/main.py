import argparse
import logging
import glob, os
import ImageTiler, TileScoring, BoundingBox, FinalImageWriter

LOG_FILE_NAME="log.txt"
LOG_FILE_MODE="w"
LOG_FORMAT="%(name)s - %(levelname)s - %(message)s"

logging.basicConfig(level=logging.INFO)
# logging.basicConfig(filename=LOG_FILE_NAME, filemode=LOG_FILE_MODE, format=LOG_FORMAT, level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Utility to help with analysis of high-resolution images when using the Custom Vision API.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--train", help="If present, only tiles the source image but does not score. Used for generating training images", action="store_true")
    group.add_argument("-s", "--score", help="If present, tiles the source image and scores against the Custom Vision API, generating a final image with object identification rectangles overlayed.", action="store_true")
    parser.add_argument("sourceImage", help="The path to the source image to create tiles from.", type=str)
    parser.add_argument("tileOutputPath", help="The output path to save the tiles to.", type=str)
    parser.add_argument("tileHeight", help="The height (in pixels) of each output tile", type=int)
    parser.add_argument("tileWidth", help="The width (in pixels) of each output tile", type=int)
    args = parser.parse_args()

    logging.info("Starting tiling utility with the following arguments:")
    logging.info(f"train = {args.train}")
    logging.info(f"score = {args.score}")
    logging.info(f"sourceImage = {args.sourceImage}")
    logging.info(f"tileOutputPath = {args.tileOutputPath}" )
    logging.info(f"tileHeight = {args.tileHeight}" )
    logging.info(f"tileWidth = {args.tileWidth}" )    

    # 1. Tile the input image
    tiler = ImageTiler.ImageTiler()
    scoring = TileScoring.TileScoring();
    boundingBox = BoundingBox.BoundingBox();
    finalImageWriter = FinalImageWriter.FinalImageWriter()
    tiler.WriteTiles(args.sourceImage, args.tileOutputPath, args.tileHeight, args.tileWidth, args.train)

    # 2. Call the model API endpoint
    if args.score:
        # Let's think through how this may get used from the end-user point of view...
        # Some different decisions here once we get solid model performance
        scores = scoring.ScoreTiles(args.tileOutputPath)
        boxes = boundingBox.CombineBoundingBoxes(scores)
        finalImageWriter.WriteFinalImage(args.sourceImage, boxes)

if __name__=='__main__':
    main()