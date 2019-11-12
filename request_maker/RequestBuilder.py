
"""

"""

from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import requests
import logging
import aiohttp
import asyncio

logging.basicConfig(level=logging.INFO)
module_logger = logging.getLogger('starship-recommendation.request_maker')
module_logger.setLevel(logging.INFO)


class SyncRequestMaker:

    """

    """

    header = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
                          "Accept-Encoding": "gzip, deflate, sdch"}

    def __init__(self, total_retries, backoff_factor):
        self.logger = logging.getLogger("starship-recommendation.request_maker.SyncRequestMaker")
        self.logger.setLevel(logging.INFO)
        self.total_retries = total_retries
        self.backoff_factor = backoff_factor
        self.logger.info("setting up total retries to {0} and the backoff_factor to {1}".format(total_retries,
                                                                                           backoff_factor))

    def retry(self):
        retries = Retry(
                total=self.total_retries,
                backoff_factor=self.backoff_factor,
                status_forcelist=[422, 500, 502, 503, 504, 429, 409, 404]
        )
        return retries

    def session_builder(self):
        retries = self.retry()
        session = requests.Session()
        session.header = self.header
        session.mount('https://', HTTPAdapter(max_retries=retries))
        session.mount('http://', HTTPAdapter(max_retries=retries))
        self.logger("created new session object")
        return session

    def make_request(self, url):
        self.logger.info("preparing to crawl {}".format(url))
        session = self.session_builder()
        r = session.get(url)
        if r.status_code == 200:
            self.logger.info("successfully crawled {0}".format(r.url))
            return r
        else:
            self.logger.warning("Something went wrong with {0}, "
                                "it has returned a status code {1},"
                                "and the following headers {2}".format(r.url, r.status_code, r.headers))


class AsyncRequestMaker:

    """

    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    timeout = aiohttp.ClientTimeout(total=60)

    def __init__(self):
        self.logger = logging.getLogger("starship-recommendation.request_maker.AsyncRequestMaker")
        self.logger.setLevel(logging.INFO)
        self.logger.info('creating an instance of AsyncRequestMaker')

    async def request_maker(self, session, url):
        try:
            self.logger.info("call the following URL: {0}".format(url))
            async with session.get(url, raise_for_status=True) as response:
                return await response.json()
        except aiohttp.ClientResponseError as e:
            self.logger.warning("Something went wrong with {0}. The following exception was raised {1}".format(url, e))
            return None

    async def request_consumer(self, session, urls):
        results = await asyncio.gather(*[self.request_maker(session, url)
                                         for url in urls])
        return results

    async def fetch_all(self, urls):
        async with aiohttp.ClientSession(headers=self.headers,
                                         timeout=self.timeout) as session:
            responses = await self.request_consumer(session, urls)
            return responses

    def run_fetch_all(self, urls):
        self.logger.info("creating new event loop")
        loop = asyncio.new_event_loop()
        results = loop.run_until_complete(self.fetch_all(urls))
        loop.close()
        self.logger.info("closing event loop")
        return results


if __name__ == "__main__":
    links = ['http://cnn.com',
             'http://google.com',
             'http://twitter.com']

    test = AsyncRequestMaker()
    output = test.run_fetch_all(links)
    print(output)
