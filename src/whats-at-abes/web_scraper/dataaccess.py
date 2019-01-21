# Import Libraries
import urllib3
import pprint
import boto3
from boto3.dynamodb.conditions import Key
import sys
from datetime import datetime
from collections import defaultdict

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
        return response['Items']

    def get_tables(self):
        pp.pprint("get_tables")
        response = self.dynamodb_client.list_tables()
        pp.pprint(response)
        return True

    def get_formatted_location_data(self):
        pp.pprint("get_formatted_location_data")
        location_data = self.get_all_active_items_sorted_by_location()
        location_groups = defaultdict(list)
        for item in location_data:
            category_group = location_groups[item['location']]
            if not category_group:
                category_group = defaultdict(list)

            category_group[item['category']].append(item)
            location_groups[item['location']] = category_group

        pp.pprint(location_groups)
        return location_groups

    def get_all_items_by_location_sorted_by_item_name(self, location):
        pp.pprint("get_all_items_by_location_sorted_by_item_name")
        response = self.table.query(
            IndexName='location-sort-index',
            KeyConditionExpression=Key('location').eq(location)
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
            KeyConditionExpression=Key('id').eq(item_name) &
            Key('sort').begins_with(f'{item_name}#{location}#')
        )
        pp.pprint(response)
        return response['Items']

    def get_all_notifications_by_notification_address(self, notification_address):
        pp.pprint("get_all_notifications_by_notification_address")
        response = self.table.query(
            IndexName='notification_address-sort-index',
            KeyConditionExpression=Key('notification_address').eq(notification_address)
        )
        pp.pprint(response)
        return True

    def insert_item(self, item_name, description, category):
        response = self.table.put_item(
            Item={
                'id': item_name,
                'sort': item_name,
                'item_name': item_name,
                'description': description,
                'category': category,
                'date_added': '2018-01-01'
            })
        pp.pprint(f'insert_item {response}')
        return True

    def bulk_insert(self, items):
        pp.pprint('--bulk insert items--')
        pp.pprint(items)
        pp.pprint('^^bulk insert items^^')
        current_date = datetime.utcnow().isoformat()
        with self.table.batch_writer() as batch:
            for item in items:
                pp.pprint(item)
                burger_name = item['burger_name']
                location = item['location']
                description = ' '.join(item['description'])
                category = item['category']
                location_sort_key = f'{burger_name}#{location}'
                batch.put_item(
                    Item={
                        'id': burger_name,
                        'sort': burger_name,
                        'item_name': burger_name,
                        'description': description,
                        'date_added': current_date
                    }
                )
                batch.put_item(
                    Item={
                        'id': burger_name,
                        'sort': location_sort_key,
                        'description': description,
                        'category': category,
                        'location': location,
                        'date_added': current_date
                    }
                )

    def add_location(self, location):
        pp.pprint("add_location")
        locationName = location['locationName']
        anchorText = location['anchorText']
        locationOrder = location['locationOrder']
        location_record = {
            'id': locationName,
            'sort': f'#{locationName}',
            'location': locationName,
            'anchorText': anchorText,
            'locationOrder': locationOrder
        }

        if 'url' in location:
            location_record['url'] = location['url']
            location_record['directionsUrl'] = location['directionsUrl']

        response = self.table.put_item(Item=location_record)
        pp.pprint(response)
        return True
        
    def set_item_availability(self, item_name, location, category):
        pp.pprint("set_item_availability")
        response = self.table.put_item(
            Item={
                'id': item_name,
                'sort': f'{item_name}#{location}',
                'location': location,
                'category': category,
                'date_added': datetime.utcnow().isoformat()
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
