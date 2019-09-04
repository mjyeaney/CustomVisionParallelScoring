import logging, os
import glob
import time
import random
import asyncio

from datetime import timedelta
from tornado import gen, httpclient, ioloop, queues

TASK_CONCURRENCY = 5
WORK_QUEUE_TIMEOUT_SEC = 300

class ParallelScoringMethod:
    """
    Implements scoring calls against the Custom Vision API in a parallel manner.
    """

    tiles = []
    scores = []

    async def __sendApiRequest(self, tileName):
        await asyncio.sleep(.750)
        logging.info(f"Scoring tile {tileName}...")
        # TODO: Make sdk call here instead - mock calls for now
        _, index, tileRow, tileCol, angle = tileName.split('.')[0].split('_')
        self.scores.append({
            "name": tileName,
            "score": random.random(),
            "tileRow": int(tileRow),
            "tileColumn": int(tileCol),
            "boxes": [
                (100.0, 100.0, 200.0, 200.0),
                (300.0, 300.0, 350.0, 500.0)
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