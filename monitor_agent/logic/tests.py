import asyncio
import unittest

from monitor_agent.logic import reader
from monitor_agent.logic.scraper import ScrapeLogic


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_scrape_logic(self):
        # async def scrape_logic_tst():
        #     await ScrapeLogic.scrape_forever()
        #
        # asyncio.run(scrape_logic_tst())
        pass

    def test_get_targets(self):
        result = reader.get_targets()
        [print(r.is_being_scan) for r in result]
        self.assertEqual(type(result), list)


if __name__ == '__main__':
    unittest.main()
