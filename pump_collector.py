from scrapers.pump_factory import PumpFactory


PUMPS = [
    ("biopetrol", "http://ec2-3-22-240-207.us-east-2.compute.amazonaws.com/guiasaldos/main/donde/134"),
    ("genex", "https://genex.com.bo/estaciones/?2729_product_cat%5B0%5D=289&2729_filtered=true"),
]


def lambda_handler(event, context):
    for pump, url in PUMPS:
        scraper = PumpFactory.get_scraper(page_type=pump, url=url)
        results = scraper.parse()
        print(results)


if __name__ == "__main__":
    event = {}
    context = None
    lambda_handler(event=event, context=context)
