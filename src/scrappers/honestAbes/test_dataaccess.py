from __future__ import print_function
import unittest
import mock
from dataaccess import DataAccess
import pprint

pp = pprint.PrettyPrinter(indent=4)

burger_name = 'The Bounty Hunger'
burger_ingredients = 'grilled salami / pineapple / bbq sauce / roasted garlic & onion cream cheese'
location = '27th St'
notification_address = '4022172224'
class TestDataAccess(unittest.TestCase):

    def setUp(self):
        self.data = DataAccess()

    def test_GetAllActiveItemsSortedByLocation(self):
        result = self.data.get_all_active_items_sorted_by_location()
        self.assertTrue(result)

    def test_GetAllItemsByLocationSortedByItemName(self):
        result = self.data.get_all_items_by_location_sorted_by_item_name(location)
        self.assertTrue(result)

    def test_GetAllUniqueItems(self):
        result = self.data.get_all_unique_items()
        self.assertTrue(result)

    def test_GetAllNotificationsByItemLocation(self):
        result = self.data.get_all_notifications_by_item_and_location(burger_name, location)
        print(result)
        self.assertTrue(True)

    def test_GetAllNotificationsByNotificationAddress(self):
        result = self.data.get_all_notifications_by_notification_address(notification_address)
        self.assertTrue(result)
    
    def test_insert_item(self):
        result = self.data.insert_item(burger_name,burger_ingredients)
        self.assertTrue(result)

    def test_set_item_availability(self):
        result = self.data.set_item_availability(burger_name,  location, 'Burger of the Week')
        self.assertTrue(result)

    def test_add_notification(self):
        result = self.data.add_notification(notification_address, burger_name, location)
        self.assertTrue(result)

    def test_remove_notification(self):
        result = self.data.remove_notification(notification_address, burger_name, location)
        self.assertTrue(result)