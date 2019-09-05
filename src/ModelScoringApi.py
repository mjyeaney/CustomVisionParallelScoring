import logging, os
import glob
import time
import random
import asyncio

from datetime import timedelta
from tornado import gen, httpclient, ioloop, queues

from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

# Async/tornado settings
TASK_CONCURRENCY = 5
WORK_QUEUE_TIMEOUT_SEC = 300

class ParallelScoringMethod:
    """
    Implements scoring calls against the Custom Vision API in a parallel manner.
    """

    tiles = []
    scores = []

    async def __sendApiRequest(self, tileName):
        logging.info(f"Scoring tile {tileName}...")

        # Disassemble tile name so we can build results collections
        _, index, tileRow, tileCol, angle = tileName.split('.')[0].split('_')
  
        # Now there is a trained endpoint that can be used to make a prediction
        predictor = CustomVisionPredictionClient(prediction_key, endpoint=SERVICE_ENDPOINT)

        # Open the sample image and get back the prediction results.
        with open(tileName, mode="rb") as test_data:
            results = predictor.detect_image(project_id, publish_iteration_name, test_data)

        # Capture the results.    
        for prediction in results.predictions:
            score = prediction.probability * 100
            x1 = prediction.bounding_box.left * 800
            y1 = prediction.bounding_box.top * 600
            x2 = x1 + (prediction.bounding_box.width * 800)
            y2 = y1 + (prediction.bounding_box.height * 600)

            if (score > scoring_threshold):
                logging.info(f"Found box at ({x1}, {y1}, {x2}, {y2}) with probability {score}")
        
                self.scores.append({
                    "name": tileName,
                    "score": score,
                    "tileRow": int(tileRow),
                    "tileColumn": int(tileCol),
                    "boxes": [
                        (x1, y1, x2, y2)
                    ]
                })

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
                    logging.error(f"Exception: {e} {tileName}")
                finally:
                    q.task_done()

        # Enqueue each tile path/name for workers to grab
        for tile in self.tiles:
            await q.put(tile)

        # Start workers, then wait for the work queue to be empty.
        workers = gen.multi([worker() for _ in range(TASK_CONCURRENCY)])
        await q.join(timeout=timedelta(seconds=WORK_QUEUE_TIMEOUT_SEC))
        assert fetching == fetched
        logging.info(f"Done in {(time.time() - start)} seconds, fetched {len(fetched)} URLs.")

        # Signal all the workers to exit.
        for _ in range(TASK_CONCURRENCY):
            await q.put(None)

        # wait for workers
        await workers

    def ScoreTiles(self, tileDirectory):
        """
        Reads the tiles from the specified directory, and sends those to the scoring API endpoint in parallel.
        """

        self.tiles = glob.glob(os.path.join(tileDirectory, "*.png"))
        logging.info(f"Found {len(self.tiles)} tiles for scoring...")

        io_loop = ioloop.IOLoop.current()
        io_loop.run_sync(self.__doWork)

        return self.scores