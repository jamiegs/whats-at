# -*- coding: utf-8 -*-
# Import Libraries
import urllib3
import json
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import pprint
from dataaccess import DataAccess

pp = pprint.PrettyPrinter(indent=4)
location_data_file = 'location_data.json'

rotating_burger_selector = '#et-boc > div > div.et_pb_section.et_pb_section_4.menuToggles.et_section_regular > div.et_pb_row.et_pb_row_8.et_pb_equal_columns.et_pb_gutters1.et_pb_row_fullwidth > div.et_pb_column.et_pb_column_1_2.et_pb_column_11.et_pb_css_mix_blend_mode_passthrough > div > div'
rotating_burger_selector2 ='#et-boc > div > div.et_pb_section.et_pb_section_4.menuToggles.et_section_regular > div.et_pb_row.et_pb_row_10.et_pb_equal_columns.et_pb_gutters1.et_pb_row_fullwidth > div.et_pb_column.et_pb_column_1_2.et_pb_column_14.et_pb_css_mix_blend_mode_passthrough > div'
burger_of_week_selector = '#et-boc > div > div.et_pb_section.et_pb_section_4.menuToggles.et_section_regular > div.et_pb_row.et_pb_row_9.et_pb_equal_columns.et_pb_gutters1.et_pb_row_fullwidth > div.et_pb_column.et_pb_column_1_2.et_pb_column_13.et_pb_css_mix_blend_mode_passthrough > div > div'
classic_burger_selector = '#et-boc > div > div.et_pb_section.et_pb_section_4.menuToggles.et_section_regular > div.et_pb_row.et_pb_row_7.et_pb_equal_columns.et_pb_gutters1.et_pb_row_fullwidth > div.et_pb_column.et_pb_column_1_2.et_pb_column_9.et_pb_css_mix_blend_mode_passthrough > div > div'
rotating_burger_xpath = '//*[@id="et-boc"]/div/div[5]/div[2]/div[1]/div'

rotating_burgers_class='rotatingBurgersToggle'
classic_burgers_class='burgersToggle'
fries_class='friesToggle'

items_to_ignore = [
    'The Honest Salad',
    'Parmesan Truffle Fries $3.25',
    'Lil’ Kids Meal'
]

class Scraper:
    def __init__(self):
        self.data = DataAccess()
        self.location_data = None

    def get_class(self, soup_content, tag, class_to_search):
        mydivs = soup_content.findAll(tag, {"class": class_to_search})
        return mydivs

    def load_location_data(self):
        with open(location_data_file) as f:
            file_data = json.load(f)
        self.location_data = file_data
        print('File read Location data:')
        print(self.location_data)
        for location in self.location_data:
            self.data.add_location(location)

    def parse_category(self, content, location):
        burgers = list()
        current_burger_name = None
        description_text = []
        html_category_name = None
        category_title_content = self.get_class(content, 'h5', 'et_pb_toggle_title')
        for result in category_title_content:
            for title_children in result.children:        
                    if 'NavigableString' in str(type(title_children)):
                        # Parse CategoryName
                        html_category_name = title_children

        category_content = self.get_class(content, 'div', 'et_pb_toggle_content')
        for result in category_content:
            for burger_children in result.children:
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
                                            'category': html_category_name,
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
                'category': html_category_name,
                'location': location
            })
        return burgers

    def parse_page(self, content, location):
        print(f'Getting burgers from {location}.')
        burgers = list()

        soup = BeautifulSoup(content, 'lxml')
        
        rotating_burgers_divs = self.get_class(soup, 'div', rotating_burgers_class)

        for rotating_burgers_div in rotating_burgers_divs:
            burgers_retrieved = self.parse_category(rotating_burgers_div, location)
            burgers.extend(burgers_retrieved)

        classic_burgers_divs = self.get_class(soup, 'div', classic_burgers_class)
        for classic_burgers_div in classic_burgers_divs:
            burgers_retrieved = self.parse_category(classic_burgers_div, location)
            burgers.extend(burgers_retrieved)

        fries_divs = self.get_class(soup, 'div', fries_class)
        for fries_div in fries_divs:
            fries_retrieved = self.parse_category(fries_div, location)
            burgers.extend(fries_retrieved)

        pp.pprint(burgers)
        return burgers


    def remove_useless_items(self, menu_items):
        filtered_menu_items = list()

        for menu_item in menu_items:
            if not menu_item['burger_name'] in items_to_ignore:
                    filtered_menu_items.append(menu_item)

        return filtered_menu_items

    def recategorize_rotating_fries(self, menu_items):
        for menu_item in menu_items:
            if menu_item['category'] == 'Fries':
                    menu_item['category'] = 'Rotating Fries'

        return menu_items

    def populate_burgers(self, url, location):
        burgers = self.read_page(url, location)
        burgers = self.remove_useless_items(burgers)
        burgers = self.group_classics(burgers)
        burgers = self.recategorize_rotating_fries(burgers)

        if burgers:
            self.data.bulk_insert(burgers)
        else:
            print('No burgers found.')

    def populate_all_burgers(self):
        all_burgers = list()
        if self.location_data:
            for location in self.location_data:
                if 'url' in location:
                    print(f'Reading Page {location}')
                    burgers = self.read_page(location['url'], location['locationName'])
                    burgers = self.remove_useless_items(burgers)
                    burgers = self.group_classics(burgers)
                    burgers = self.recategorize_rotating_fries(burgers)

                    if burgers:
                        self.data.bulk_insert(burgers)
                        burgers.extend(burgers)
                    else:
                        print(f"No burgers found for location {location['locationName']}")
        return all_burgers

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
