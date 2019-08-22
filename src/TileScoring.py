import logging, os
import glob
import time
from datetime import timedelta
from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag
from tornado import gen, httpclient, ioloop, queues

base_url = "http://www.tornadoweb.org/en/stable/"
concurrency = 5

class TileScoring:

    tiles = []

    async def get_links_from_url(self, url):
        response = await httpclient.AsyncHTTPClient().fetch(url)
        logging.info(f"HTTP GET: {url}, status = {response.code}")
        html = response.body.decode(errors="ignore")

    async def __doWork(self):
        start = time.time()
        q = queues.Queue()
        fetching, fetched = [], []

        async def fetch_url(current_url):
            # logging.info(f"Fetching {current_url}...")
            fetching.append(current_url)
            await self.get_links_from_url(current_url)
            fetched.append(current_url)

        async def worker():
            async for url in q:
                if url is None:
                    return
                try:
                    await fetch_url(url)
                except Exception as e:
                    logging.error(f"Exception: {e} {url}")
                finally:
                    q.task_done()

        for tile in self.tiles:
            await q.put(base_url)

        # Start workers, then wait for the work queue to be empty.
        workers = gen.multi([worker() for _ in range(concurrency)])
        await q.join(timeout=timedelta(seconds=300))
        assert fetching == fetched
        logging.info(f"Done in {(time.time() - start)} seconds, fetched {len(fetched)} URLs.")

        # Signal all the workers to exit.
        for _ in range(concurrency):
            await q.put(None)

        # wait for workers
        await workers

    def ScoreTiles(self, tileDirectory):
        self.tiles = glob.glob(os.path.join(tileDirectory, "*.png"))
        logging.info(f"Found {len(self.tiles)} tiles for scoring...")

        io_loop = ioloop.IOLoop.current()
        io_loop.run_sync(self.__doWork)