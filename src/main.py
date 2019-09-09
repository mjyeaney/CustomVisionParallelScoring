import argparse
import logging
import glob, os

from ImageTiling import DefaultImageTiler
from ModelScoring import ParallelScoring
from BoundingBoxes import CoordinateOperations
from ResultsWriter import ImageWithBoundingBoxes
from Settings import ConfigSettings

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
        "--outputPath", 
        help="The path to write the final output image to when scoring (using the '-s' or '--score' flags)", 
        type=str, 
        default=""
    )
    args = parser.parse_args()

    logging.info("Starting tiling utility with the following arguments:")
    logging.info(f"train = {args.train}")
    logging.info(f"score = {args.score}")
    logging.info(f"sourceImage = {args.sourceImage}")
    logging.info(f"tileWidth = {args.tileWidth}") 
    logging.info(f"tileHeight = {args.tileHeight}")
    logging.info(f"outputPath = {args.outputPath}")

    # Quick validation check
    if args.score:
        # Make sure we have the final output path available
        if args.outputPath == "":
            raise Exception("Missing '--outputPath' argument!!!")

    # Applicaiton services
    settings = ConfigSettings(os.path.abspath("./settings.cfg"))
    tiler = DefaultImageTiler(settings, args.tileHeight, args.tileWidth)
    scoringMethod = ParallelScoring(settings, args.tileWidth, args.tileHeight)
    coordinateOps = CoordinateOperations()
    resultsWriter = ImageWithBoundingBoxes()

    # Verify / dump settings
    settings.DumpSettingsToLog()

    # Cleanup any leftover temp files
    tiler.Cleanup()

    # Tile the input image
    tiler.CreateTiles(
        args.sourceImage, 
        args.train
    )

    # If scoring, run the scoring workflow
    if args.score:        
        scores = scoringMethod.ScoreTiles()
        boxes = coordinateOps.RemapBoundingBoxes(args.tileHeight, args.tileWidth, scores)
        resultFileName = os.path.join(args.outputPath, os.path.basename(args.sourceImage))
        resultsWriter.Write(args.sourceImage, boxes, resultFileName)

        # Cleanup (only when scoring)
        tiler.Cleanup()

if __name__=='__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"{e}")