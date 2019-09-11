import logging, os
import glob
import time
import random
import asyncio
import configparser

from datetime import timedelta
from tornado import gen, httpclient, ioloop, queues
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

# Async/tornado settings
TASK_CONCURRENCY = 5
WORK_QUEUE_TIMEOUT_SEC = 300

logger = logging.getLogger("ModelScoring")

class ParallelScoring:
    """
    Implements scoring calls against the Custom Vision API in a parallel manner.
    """

    def __init__(self, settings, tileWidth, tileHeight):
        self.tiles = []
        self.scores = []
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.tempFilePath = settings.tempFilePath

        # Grab configuration settings
        self.serviceEndpoint = settings.serviceEndpoint
        self.predictionKey = settings.predictionKey
        self.predictionResourceId = settings.predictionResourceId
        self.publishIterationName = settings.publishIterationName
        self.projectId = settings.projectId
        self.boundingBoxScoreThreshold = settings.boundingBoxScoreThreshold

    async def __sendApiRequest(self, tileName):
        logger.info(f"Scoring tile {tileName}...")

        # Disassemble tile name so we can build results collections
        _, index, tileRow, tileCol, angle = tileName.split('.')[0].split('_')
  
        # Now there is a trained endpoint that can be used to make a prediction
        predictor = CustomVisionPredictionClient(self.predictionKey, endpoint=self.serviceEndpoint)

        # Open the sample image and get back the prediction results.
        with open(tileName, mode="rb") as test_data:
            logger.info(await httpclient.AsyncHTTPClient().fetch(method="PUT", body=test_data, request=self.serviceEndpoint).body)
            # html = response.body.decode(errors="ignore")
            results = predictor.detect_image(self.projectId, self.publishIterationName, test_data)

        # Capture the results.    
        for prediction in results.predictions:
            score = prediction.probability * 100
            x1 = prediction.bounding_box.left * self.tileWidth
            y1 = prediction.bounding_box.top * self.tileHeight
            x2 = x1 + (prediction.bounding_box.width * self.tileWidth)
            y2 = y1 + (prediction.bounding_box.height * self.tileHeight)

            if (score > self.boundingBoxScoreThreshold):
                logger.info(f"Found box at ({x1}, {y1}, {x2}, {y2}) with probability {score}")
        
                self.scores.append({
                    "name": tileName,
                    "score": score,
                    "tileRow": int(tileRow),
                    "tileColumn": int(tileCol),
                    "boxes": [
                        (x1, y1, x2, y2)
                    ]
                })
            else:
                logger.info(f"**Skipping box with threshold {score}**")

    async def __doWork(self):
        start = time.time()
        q = queues.Queue()
        fetching, fetched = [], []

        async def score(tileName):
            fetching.append(tileName)
            await self.__sendApiRequest(tileName)
            fetched.append(tileName)

        async def worker():
            async for tileName in q:
                if tileName is None:
                    return
                try:
                    await score(tileName)
                except Exception as e:
                    logger.error(f"Exception: {e} {tileName}")
                finally:
                    q.task_done()

        # Enqueue each tile path/name for workers to grab
        for tile in self.tiles:
            await q.put(tile)

        # Start workers, then wait for the work queue to be empty.
        workers = gen.multi([worker() for _ in range(TASK_CONCURRENCY)])
        await q.join(timeout=timedelta(seconds=WORK_QUEUE_TIMEOUT_SEC))
        assert fetching == fetched
        logger.info(f"Done in {(time.time() - start)} seconds, fetched {len(fetched)} URLs.")

        # Signal all the workers to exit.
        for _ in range(TASK_CONCURRENCY):
            await q.put(None)

        # wait for workers
        await workers

    def ScoreTiles(self):
        """
        Reads the tiles from the specified directory, and sends those to the scoring API endpoint in parallel.
        """

        self.tiles = glob.glob(os.path.join(self.tempFilePath, "*.png"))
        logger.info(f"Found {len(self.tiles)} tiles for scoring...")

        io_loop = ioloop.IOLoop.current()
        io_loop.run_sync(self.__doWork)

        return self.scores