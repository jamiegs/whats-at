from scraper import Scraper

def lambda_handler(event, context):
    scraper = Scraper()
    scraper.populate_all_burgers()