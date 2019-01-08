# -*- coding: utf-8 -*-
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape

def main():
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    print(template)
    print(template.render(the='variables', go='here'))


main()