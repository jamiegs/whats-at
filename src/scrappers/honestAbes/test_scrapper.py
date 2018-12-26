from __future__ import print_function
import unittest
import mock
from scrapper import Scrapper
import pprint

pp = pprint.PrettyPrinter(indent=4)

class TestScrapper(unittest.TestCase):
    def setUp(self):
        self.scrapper = Scrapper()

    def test_populate_burgers(self):
        self.scrapper.populate_burgers('http://grounduprestaurants.com/honest-abes-meadowlane/', 'Meadowlane')


    def test_parse_page(self):
        classic_burger_Category = "Classic Burgers"
        rotating_burger_category = 'Rotating Burgers'
        burger_of_week_category = 'Burger of the Week'

        name_greatestBurger = 'Greatest Burger Ever'
        contains_greatestBurger = False
        category_greatestBurger = classic_burger_Category

        name_8second = '8 Second'
        contains_8second = False
        category_8second = rotating_burger_category

        name_anotherBrick = 'Another Brick in the Walnut'
        contains_anotherBrick = False
        category_anotherBrick = rotating_burger_category

        name_morningGlory = 'Morning Glory'
        contains_morningGlory = False
        category_morningGlory = rotating_burger_category

        name_oktolieber = 'Okto-lieber'
        contains_oktolieber = False
        category_oktolieber = rotating_burger_category

        name_barkeep = 'Barkeep’s Choice'
        contains_barkeep = False
        category_barkeep = burger_of_week_category

        contents = self.read_file('test_page.html')
        location = "North 27th St."
        items = self.scrapper.parse_page(contents, location)

        for item in items:

            pp.pprint(f"{item['burger_name']} description: {item['description']} category: {item['category']} location: {item['location']}")
            
            self.assertEqual(item['location'], location)

            if item['burger_name'] == name_greatestBurger:
                contains_greatestBurger = True
                self.assertEqual(item['category'], category_greatestBurger)
    
            if item['burger_name'] == name_8second:
                contains_8second = True
                self.assertEqual(item['category'], category_8second)

            elif item['burger_name'] == name_anotherBrick:
                contains_anotherBrick = True
                self.assertEqual(item['category'], category_anotherBrick)
        
            elif item['burger_name'] == name_morningGlory:
                contains_morningGlory = True
                self.assertEqual(item['category'], category_morningGlory)
        
            elif item['burger_name'] == name_oktolieber:
                contains_oktolieber = True
                self.assertEqual(item['category'], category_oktolieber)
        
            elif item['burger_name'] == name_barkeep:
                contains_barkeep = True
                self.assertEqual(item['category'], category_barkeep)

        self.assertTrue(contains_greatestBurger)
        self.assertTrue(contains_8second)
        self.assertTrue(contains_anotherBrick)
        self.assertTrue(contains_morningGlory)
        self.assertTrue(contains_oktolieber)
        self.assertTrue(contains_barkeep)


    def read_file(self, filename):
        with open(filename) as f:
            content = f.read()
        return str(content)
