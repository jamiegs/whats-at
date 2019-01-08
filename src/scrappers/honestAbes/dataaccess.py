# Import Libraries
import urllib3
import pprint
import boto3
from boto3.dynamodb.conditions import Key
import sys

sys.setrecursionlimit(10000)
pp = pprint.PrettyPrinter(indent=4)

TABLE_NAME = "WhatsAt-master3"
REGION = "us-east-1"

class DataAccess:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.dynamodb_client = boto3.client('dynamodb')
        self.table = self.dynamodb.Table(TABLE_NAME)

    def get_all_active_items_sorted_by_location(self):
        pp.pprint("get_all_active_items_sorted_by_location")
        response = self.table.scan(
            IndexName='location-sort-index'
            )
        pp.pprint(response)
        return True

    def get_tables(self):
        pp.pprint("get_all_active_items_sorted_by_location")
        response = self.dynamodb_client.list_tables()
        pp.pprint(response)
        return True

    def get_all_items_by_location_sorted_by_item_name(self, location):
        pp.pprint("get_all_items_by_location_sorted_by_item_name")
        response = self.table.query(
            IndexName='location-sort-index',
            KeyConditionExpression=
                Key('location').eq(location)
            )
        pp.pprint(response)
        return True

    def get_all_unique_items(self):
        response = self.table.scan(
            Select='ALL_ATTRIBUTES'
        )
        pp.pprint(response)
        return True

    def get_all_notifications_by_item_and_location(self, item_name, location):
        response = self.table.query(
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression=
                Key('id').eq(item_name) & 
                Key('sort').begins_with(f'{item_name}#{location}#')
            )
        pp.pprint(response)
        return response['Items']

    def get_all_notifications_by_notification_address(self, notification_address):
        pp.pprint("get_all_notifications_by_notification_address")
        response = self.table.query(
            IndexName='notification_address-sort-index',
            KeyConditionExpression=
                Key('notification_address').eq(notification_address)
            )
        pp.pprint(response)
        return True

    def insert_item(self, item_name, description, category):
        response = self.table.put_item(
            Item={
                'id': item_name,
                'sort': item_name,
                'item_name': item_name,
                'description':  description,
                'category': category,
                'date_added': '2018-01-01'
            })
        pp.pprint(f'insert_item {response}')
        return True

    def bulk_insert(self, items):
        with self.table.batch_writer() as batch:
            for item in items:
                batch.put_item(
                            Item={
                            'id': item['burger_name'],
                            'sort': item['burger_name'],
                            'item_name': item['burger_name'],
                            'description':  item['description'],
                            'category': item['category'],
                            'date_added': '2018-01-01'
                        }
                )

    def set_item_availability(self, item_name, location, category):
        pp.pprint("set_item_availability")
        response = self.table.put_item(
        Item={
            'id': item_name,
            'sort': f'{item_name}#{location}',
            'item_name': item_name,
            'location': location,
            'category': category,
            'date_added': '2018-01-01'
        })
        pp.pprint(response)
        return True

    def add_notification(self, notification_address, item_name, location):
        pp.pprint("add_notification")
        response = self.table.put_item(
        Item={
            'id': item_name, 
            'sort': f'{item_name}#{location}#{notification_address}', 
            'item_name': item_name,
            'notification_address': notification_address,
            'location': location,
            'date_added': '2018-01-01'
        })
        pp.pprint(response)
        return True
    
    def remove_notification(self, notification_address, item_name, location):
        pp.pprint("remove_notification")
        response = self.table.delete_item(
        Key={
            'id': item_name,
            'sort': f'{item_name}#{location}#{notification_address}'
        })
        pp.pprint(response)
        return True