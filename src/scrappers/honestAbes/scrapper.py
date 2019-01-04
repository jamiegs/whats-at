# Import Libraries
import urllib3
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import pprint
from dataaccess import DataAccess

pp = pprint.PrettyPrinter(indent=4)

location_pages = [
    {
        'locationName': 'Meadowlane',
        'url': 'http://grounduprestaurants.com/honest-abes-meadowlane/'
    },
    {
        'locationName': 'Downtown',
        'url': 'http://grounduprestaurants.com/honest-abes-downtown/'
    },
    {
        'locationName': 'Glynoaks',
        'url': 'http://grounduprestaurants.com/honest-abes-glynoaks/'
    },
    {
        'locationName': '27th St',
        'url': 'http://grounduprestaurants.com/honest-abes-north-27th/'
    }
]
rotating_burger_selector = '#et-boc > div > div.et_pb_section.et_pb_section_4.menuToggles.et_section_regular > div.et_pb_row.et_pb_row_8.et_pb_equal_columns.et_pb_gutters1.et_pb_row_fullwidth > div.et_pb_column.et_pb_column_1_2.et_pb_column_11.et_pb_css_mix_blend_mode_passthrough > div > div'
burger_of_week_selector = '#et-boc > div > div.et_pb_section.et_pb_section_4.menuToggles.et_section_regular > div.et_pb_row.et_pb_row_9.et_pb_equal_columns.et_pb_gutters1.et_pb_row_fullwidth > div.et_pb_column.et_pb_column_1_2.et_pb_column_13.et_pb_css_mix_blend_mode_passthrough > div > div'
classic_burger_selector = '#et-boc > div > div.et_pb_section.et_pb_section_4.menuToggles.et_section_regular > div.et_pb_row.et_pb_row_7.et_pb_equal_columns.et_pb_gutters1.et_pb_row_fullwidth > div.et_pb_column.et_pb_column_1_2.et_pb_column_9.et_pb_css_mix_blend_mode_passthrough > div > div'

class Scrapper:
    def __init__(self):
        self.data = DataAccess()

    def parse_category(self, content, category, location):
        burgers = list()
        #pp.pprint(f'====category {category}====')
        #pp.pprint(content)
        #pp.pprint(f'^^^^category {category}^^^^')
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
        for location in location_pages:
            print(f'Reading Page {location}')
            burgers = self.read_page(location['url'], location['locationName'])
            if burgers:
                self.data.bulk_insert(burgers)
            else:
                print(f"No burgers found for location {location['locationName']}")

#    def main():
#    #read_all_pages()
#    read_file()

    def read_all_pages(self):
        for location in location_pages:
            print(f'Reading Page {location}')
            self.read_page(location['url'], location['locationName'])

    def read_page(self, url, location):
        http = urllib3.PoolManager()
        r = http.request('GET', url)
        page_content = str(r.data.decode('utf-8'))
        r.release_conn()
        return self.parse_page(page_content, location)

#def read_file():
#    filename = 'test_page.html'
#    with open(filename) as f:
#        content = f.read()
#    
#    parse_page(str(content))