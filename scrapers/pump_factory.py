from scrapers.biopetrol import BiopetrolPumpScraper
from scrapers.genex import GenexPumpScraper


class PumpFactory:
    @staticmethod
    def get_scraper(page_type, url):
        if page_type == 'biopetrol':
            return BiopetrolPumpScraper(url)
        elif page_type == 'genex':
            return GenexPumpScraper(url)
        else:
            raise ValueError(f"Factory Pump method {page_type} is not defined.")
