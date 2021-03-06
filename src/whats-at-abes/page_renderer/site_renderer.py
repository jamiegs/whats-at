# -*- coding: utf-8 -*-
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape
from dataaccess import DataAccess

class SiteRenderer:
    def render(self):
        env = Environment(
            loader=FileSystemLoader('templates'),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        dataAccess = DataAccess()
        data = dataAccess.get_formatted_location_data()
        
        template = env.get_template('template.html')
        rendered_output = template.render(locations=data)
        return rendered_output