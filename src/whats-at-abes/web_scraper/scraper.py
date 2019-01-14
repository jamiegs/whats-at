# Import Libraries
import urllib3
import json
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import pprint
from web_scraper.dataaccess import DataAccess

pp = pprint.PrettyPrinter(indent=4)
location_data_file = 'location_data.json'

rotating_burger_selector = '#et-boc > div > div.et_pb_section.et_pb_section_4.menuToggles.et_section_regular > div.et_pb_row.et_pb_row_8.et_pb_equal_columns.et_pb_gutters1.et_pb_row_fullwidth > div.et_pb_column.et_pb_column_1_2.et_pb_column_11.et_pb_css_mix_blend_mode_passthrough > div > div'
burger_of_week_selector = '#et-boc > div > div.et_pb_section.et_pb_section_4.menuToggles.et_section_regular > div.et_pb_row.et_pb_row_9.et_pb_equal_columns.et_pb_gutters1.et_pb_row_fullwidth > div.et_pb_column.et_pb_column_1_2.et_pb_column_13.et_pb_css_mix_blend_mode_passthrough > div > div'
classic_burger_selector = '#et-boc > div > div.et_pb_section.et_pb_section_4.menuToggles.et_section_regular > div.et_pb_row.et_pb_row_7.et_pb_equal_columns.et_pb_gutters1.et_pb_row_fullwidth > div.et_pb_column.et_pb_column_1_2.et_pb_column_9.et_pb_css_mix_blend_mode_passthrough > div > div'

class Scraper:
    def __init__(self):
        self.data = DataAccess()
        self.location_data = None

    def load_location_data(self):
        with open(location_data_file) as f:
            file_data = json.load(f)
        self.location_data = file_data
        print('File read Location data:')
        print(self.location_data)

    def parse_category(self, content, category, location):
        burgers = list()
        current_burger_name = None
        description_text = []

        for burger_children in content.children:
            if 'Tag' in str(type(burger_children)):
                if burger_children.name == 'h3':
                    if burger_children.contents:
                        if 'NavigableString' in str(type(burger_children.contents[0])):
                            # Parse Burger Name
                            burger_name = burger_children.contents[0]
                            if not current_burger_name == burger_name:
                                if current_burger_name and (not current_burger_name.isspace()) and description_text:
                                    burgers.append({
                                        'burger_name': current_burger_name,
                                        'description': description_text,
                                        'category': category,
                                        'location': location
                                    })
                                current_burger_name = burger_name
                                description_text = []

                if burger_children.name == 'p' or burger_children.name == 'span' or burger_children.name == 'em':
                    for description_children in burger_children.children:
                        if 'NavigableString' in str(type(description_children)):
                            if description_children and (not description_children.isspace()):
                                description_text.append(description_children)

                        if 'Tag' in str(type(description_children)):
                            description_child_text = description_children.get_text()
                            if description_child_text and (not description_child_text.isspace()):
                                description_text.append(description_child_text)

        if current_burger_name and (not current_burger_name.isspace()) and description_text:
            burgers.append({
                'burger_name': current_burger_name,
                'description': description_text,
                'category': category,
                'location': location
            })
        return burgers

    def parse_page(self, content, location):
        print(f'Getting burgers from {location}.')
        burgers = list()

        soup = BeautifulSoup(content, 'lxml') #html.parser')
        
        classic_burgers = soup.select(classic_burger_selector)
        for classic_burger_section in classic_burgers:
            burgers.extend(self.parse_category(classic_burger_section, 'Classic Burgers', location))

        rotating_burgers = soup.select(rotating_burger_selector)
        pp.pprint('==rotating_burgers===')
        pp.pprint(rotating_burgers)
        pp.pprint('^^^rotating_burgers^^^')
        for rotating_burger_section in rotating_burgers:
            burgers.extend(self.parse_category(rotating_burger_section, 'Rotating Burgers', location))
        
        burger_of_week = soup.select(burger_of_week_selector)
        for burger_of_week_section in burger_of_week:
            burgers.extend(self.parse_category(burger_of_week_section, 'Burger of the Week', location))
   
        pp.pprint(burgers)
        return burgers

    def populate_burgers(self, url, location):
        burgers = self.read_page(url, location)
        if burgers:
            self.data.bulk_insert(burgers)
        else:
            print('No burgers found.')

    def populate_all_burgers(self):
        if self.location_data:
            for location in self.location_data:
                print(f'Reading Page {location}')
                burgers = self.read_page(location['url'], location['locationName'])
                burgers = self.group_classics(burgers)
                if burgers:
                    self.data.bulk_insert(burgers)
                else:
                    print(f"No burgers found for location {location['locationName']}")

    def group_classics(self, burgers):
        for burger in burgers:
            if burger['category'] == 'Classic Burgers':
                burger['location'] = 'All Locations'

        return burgers

    def read_all_pages(self):
        for location in self.location_data:
            print(f'Reading Page {location}')
            self.read_page(location['url'], location['locationName'])

    def read_page(self, url, location):
        http = urllib3.PoolManager()
        headers = {
            'User-Agent': 'whatsatabes.com bot',
        }
        r = http.request('GET', url, headers=headers)
        page_content = str(r.data.decode('utf-8'))
        r.release_conn()
        return self.parse_page(page_content, location)
