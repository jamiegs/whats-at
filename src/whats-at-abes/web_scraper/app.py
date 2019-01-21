from web_scraper import Scraper

def lambda_handler(event, context):
    scraper = Scraper()
    scraper.load_location_data()
    return scraper.populate_all_burgers()