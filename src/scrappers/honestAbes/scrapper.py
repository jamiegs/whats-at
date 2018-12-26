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
rotating_burger_selector = '#et-boc > div > div.et_pb_section.et_pb_section_4.menuToggles.et_section_regular > div.et_pb_row.et_pb_row_8.et_pb_equal_columns.et_pb_gutters1.et_pb_row_fullwidth > div.et_pb_column.et_pb_column_1_2.et_pb_column_11.et_pb_css_mix_blend_mode_passthrough > div'
burger_of_week_selector = '#et-boc > div > div.et_pb_section.et_pb_section_4.menuToggles.et_section_regular > div.et_pb_row.et_pb_row_9.et_pb_equal_columns.et_pb_gutters1.et_pb_row_fullwidth > div.et_pb_column.et_pb_column_1_2.et_pb_column_13.et_pb_css_mix_blend_mode_passthrough > div > div'
classic_burger_selector = '#et-boc > div > div.et_pb_section.et_pb_section_4.menuToggles.et_section_regular > div.et_pb_row.et_pb_row_7.et_pb_equal_columns.et_pb_gutters1.et_pb_row_fullwidth > div.et_pb_column.et_pb_column_1_2.et_pb_column_9.et_pb_css_mix_blend_mode_passthrough > div > div'

class Scrapper:
    def __init__(self):
        self.data = DataAccess()

    def parse_burger_section(self, content, category, location):
        burgers = list()
        burger_name = ''
        description_text = ''
        for burger_children in content.descendants:
            if 'Tag' in str(type(burger_children)):
                if burger_children.name == 'h3':
                    burger_name = burger_children.get_text()

                if burger_children.name == 'p': 
                    description_text = burger_children.get_text()   

                if burger_name and (not burger_name.isspace()) and description_text and (not description_text.isspace()):
                    burgers.append({
                        'burger_name': burger_name,
                        'description': description_text,
                        'category': category,
                        'location': location
                    })
                    burger_name = ''
                    description_text = ''

        return burgers

    def parse_page(self, content, location):
        print(f'Getting burgers from {location}.')
        burgers = list()

        soup = BeautifulSoup(content, 'lxml') #html.parser')
        
        classic_burgers = soup.select(classic_burger_selector)
        for classic_burger_section in classic_burgers:
            burgers.extend(self.parse_burger_section(classic_burger_section, 'Classic Burgers', location))

        rotating_burgers = soup.select(rotating_burger_selector)
        for rotating_burger_section in rotating_burgers:
            burgers.extend(self.parse_burger_section(rotating_burger_section, 'Rotating Burgers', location))
        
        burger_of_week = soup.select(burger_of_week_selector)
        for burger_of_week_section in burger_of_week:
            burgers.extend(self.parse_burger_section(burger_of_week_section, 'Burger of the Week', location))
   
        print(burgers)
        return burgers

    def populate_burgers(self, url, location):
        burgers = self.read_page(url, location)
        if burgers:
            for burger in burgers:
                self.data.insert_item(burger['burger_name'], burger['description'])
                pp.pprint(burger)
        else:
            print('No burgers found.')
        

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
        print(page_content)
        return self.parse_page(page_content, location)

#def read_file():
#    filename = 'test_page.html'
#    with open(filename) as f:
#        content = f.read()
#    
#    parse_page(str(content))