import argparse
import logging
import glob, os

from ImageTiling import DefaultImageTiler
from ModelScoringApi import ParallelScoringMethod
from BoundingBoxes import CoordinateOperations
from ResultsWriter import ImageWithBoundingBoxes

LOG_FORMAT="%(asctime)s: %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(
        description="Utility to help with analysis of high-resolution images when using the Custom Vision API."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-t", 
        "--train", 
        help="If present, only tiles the source image but does not score. Used for generating training images", 
        action="store_true"
    )
    group.add_argument(
        "-s", 
        "--score", 
        help="If present, tiles the source image and scores against the Custom Vision API, generating a final image with object identification rectangles overlayed.", 
        action="store_true"
    )
    parser.add_argument(
        "--sourceImage", 
        help="The path to the source image to create tiles from.", 
        type=str
    )
    parser.add_argument(
        "--tileOutputPath", 
        help="The output path to save the tiles to.", 
        type=str
    )
    parser.add_argument(
        "--tileWidth", 
        help="The width (in pixels) of each output tile", 
        type=int
    )
    parser.add_argument(
        "--tileHeight", 
        help="The height (in pixels) of each output tile", 
        type=int
    )
    parser.add_argument(
        "--outputImagePath", 
        help="The path to write the final output image to when scoring (using the '-s' or '--score' flags)", 
        type=str, 
        default=""
    )
    args = parser.parse_args()

    logging.info("Starting tiling utility with the following arguments:")
    logging.info(f"train = {args.train}")
    logging.info(f"score = {args.score}")
    logging.info(f"sourceImage = {args.sourceImage}")
    logging.info(f"tileOutputPath = {args.tileOutputPath}")
    logging.info(f"tileWidth = {args.tileWidth}") 
    logging.info(f"tileHeight = {args.tileHeight}")
    logging.info(f"outputImagePath = {args.outputImagePath}") 

    # Quick validation check
    if args.score:
        # Make sure we have the final output path available
        if args.outputImagePath == "":
            raise Exception("Missing '--outputImagePath' argument!!!")

    # Applicaiton services
    tiler = DefaultImageTiler()
    scoringApi = ParallelScoringMethod()
    coordinateOps = CoordinateOperations()
    resultsWriter = ImageWithBoundingBoxes()

    # Tile the input image
    tiler.WriteTiles(
        args.sourceImage, 
        args.tileOutputPath, 
        args.tileHeight, 
        args.tileWidth, 
        args.train
    )

    # Call the model API endpoint
    if args.score:
        # Run the scoring workflow
        scores = scoringApi.ScoreTiles(args.tileOutputPath)
        boxes = coordinateOps.RemapBoundingBoxes(scores)
        resultsWriter.Write(args.sourceImage, boxes, args.outputImagePath)

if __name__=='__main__':
    main()