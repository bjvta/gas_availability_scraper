import requests


class PumpBaseScraper:
    def __init__(self, url):
        self.url = url
        self.page_content = None

    def fetch_content(self):
        response = requests.get(self.url)
        response.raise_for_status()
        self.page_content = response.content

    def parse(self):
        raise NotImplementedError("This method should be implemented")
