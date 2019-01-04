from __future__ import print_function
import unittest
import mock
from scrapper import Scrapper
import pprint
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=4)

class TestScrapper(unittest.TestCase):
    def setUp(self):
        self.scrapper = Scrapper()

    def test_populate_burgers(self):
        self.scrapper.populate_burgers('http://grounduprestaurants.com/honest-abes-meadowlane/', 'Meadowlane')

    def test_populate_all_burgers(self):
        self.scrapper.populate_all_burgers()


    def test_parse_category_rotating(self):
        content = '''
<div class="et_pb_toggle_content clearfix">
   <p>
      <span class="info">6oz Single $8.25<br />12oz Double $10.00<br />sub a handcrafted vegan patty for FREE <em>(contains oats)</em></span><br />brioche bun: <em>wheat / dairy</em><br />gluten free bun: <em>egg</em><br />vegan bun: <em>wheat / soy</em>
   </p>
   <h3>8 Second</h3>
   <p>bbq chips / bbq sauce / bacon / jalapeño / mayonnaise / cheddar cheese<br /><em>allergies: dairy / soy / egg / fish (Worcestershire)</em></p>
   <h3>Another Brick in the Walnut</h3>
   <p>honey-mustard Brussels sprouts / brie / walnuts / bacon mayonnaise<br /><em>allergies: soy / egg / dairy / tree nut</em></p>
   <h3>Morning Glory</h3>
   <p>fried egg / Canadian bacon / maple mayonnaise / American cheese / spinach<br /><em>allergies: soy / egg / dairy</em></p>
   <h3>Okto-lieber</h3>
   <p><span class="TextRun SCX22916004" lang="EN-US" xml:lang="EN-US"><span class="NormalTextRun SCX22916004">bratwurst / German beer cheese / green apple sauerkraut / pretzels</span></span><br /><em>allergies: dairy / fish (Worcestershire)</em></p>
   <h3></h3>
</div>
'''
        soup_content = BeautifulSoup(content, 'lxml')
        burgers = self.scrapper.parse_category(soup_content.contents[0].contents[0].contents[0], 'Rotating', 'Meadowlane')
        self.assertTrue(burgers)
        pp.pprint(burgers)


    def test_parse_category_classics(self):
        content = '''
<div class="et_pb_toggle_content clearfix">
   <p><span class="info">6oz Single $8.25<br/>12oz Double $10.00<br/>Sub a handcrafted vegan patty for FREE <em>(contains oats)</em></span><br/>brioche bun: <em>wheat / dairy</em><br/>gluten free bun: <em>egg</em><br/>vegan bun: <em>wheat / soy</em></p>
   <h3>Greatest Burger Ever</h3>
   <p>chopped bacon / griddled onions / awesome Sauce / American cheese / ketchup / romaine<br/><em>allergies: soy / egg / dairy</em></p>
   <h3>The Fireside</h3>
   <p>jalapeño / bacon / sriracha ketchup / cumin lime mayo / pepperjack cheese / romaine<br/><em>allergies: soy / egg / dairy</em></p>
   <h3>The Aphrodite</h3>
   <p>pickled red onions / cucumber &amp; feta yogurt sauce / tomato jam / fresh spinach<br/><em>allergies: dairy</em></p>
   <h3>1809</h3>
   <p>pickled apples / smoky sweet mayo / gouda cheese / chopped bacon<br/><em>allergies: soy / egg / dairy</em></p>
   <h3>United States of America</h3>
   <p><span class="TextRun SCX53318853" lang="EN-US" xml:lang="EN-US"><span class="NormalTextRun SCX53318853">red onion / pickles / American cheese / mayonnaise / ketchup / romaine</span></span><br/><em>allergies: dairy / soy / egg</em></p>
   <h3>Lil’ Kids Meal<br/>$5.25</h3>
   <p>Hamburger or Cheeseburger with fries &amp; juice</p>
</div>
'''
        lilkid_burger = {
            'burger_name': 'Lil’ Kids Meal',
            'category': 'Classics',
            'description': [
                'Hamburger or Cheeseburger with fries & juice'
            ],
            'location': 'Meadowlane'
        }
        has_lilkid_burger = False
        aphrodite_burger = {
            'burger_name': 'The Aphrodite',
            'category': 'Classics',
            'description': [
                            'pickled red onions / cucumber & feta yogurt sauce '
                            '/ tomato jam / fresh spinach',
                            'allergies: dairy'
                        ],
            'location': 'Meadowlane'
            }
        has_aphrodite_burger = False
        soup_content = BeautifulSoup(content, 'lxml')
        burgers = self.scrapper.parse_category(soup_content.contents[0].contents[0].contents[0], 'Classics', 'Meadowlane')
        self.assertTrue(burgers)

        for burger in burgers:
            if burger['burger_name'] == aphrodite_burger['burger_name']:
                has_aphrodite_burger = True
                self.assertEqual(burger['category'], aphrodite_burger['category'])
                self.assertEqual(burger['description'], aphrodite_burger['description'])
                self.assertEqual(burger['location'], aphrodite_burger['location'])
            if burger['burger_name'] == lilkid_burger['burger_name']:
                has_lilkid_burger = True
                self.assertEqual(burger['category'], lilkid_burger['category'])
                self.assertEqual(burger['description'], lilkid_burger['description'])
                self.assertEqual(burger['location'], lilkid_burger['location'])

        self.assertTrue(has_aphrodite_burger)
        self.assertTrue(has_lilkid_burger)


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
