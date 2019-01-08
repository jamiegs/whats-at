# -*- coding: utf-8 -*-
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape


def main():
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,
        lstrip_blocks=True
    )
    locations = [
        {
            'LocationName': '27th St',
            'Categories': [
                {
                    "CategoryName": 'Rotating',
                    'Items': [
                        {
                            'ItemName': 'Hammer Of thor',
                            'Description': 'Food'
                        },
                        {
                            'ItemName': 'Hair of the dog',
                            'Description': 'More food'
                        }
                    ]
                },
                {
                    'CategoryName': 'Burger Of Week',
                    'Items': [
                        {
                            'ItemName': 'Louisiana Purchase',
                            'Description': 'good food'
                        }
                    ]
                }
            ]
        }
    ]

    template = env.get_template('template.html')
    print(template)
    print(template.render(locations=locations))


main()
