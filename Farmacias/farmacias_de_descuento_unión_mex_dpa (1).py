# -*- coding: utf-8 -*-

import scrapy
import pycountry
import uuid
from locations.categories import Code
from locations.items import GeojsonPointItem


class FARMACIASDEDESCENTOUNIÓNSpider(scrapy.Spider):
    
    name = "farmacias_de_descuento_unión_mex_dpa"
    brand_name = "FARMACIAS DE DESCUENTO UNIÓN"
    spider_type = "chain"
    spider_chain_id = "22318"
    spider_categories = [
        Code.DRUGSTORE_OR_PHARMACY.value
    ]
    spider_countries = [
        pycountry.countries.lookup("MEX").alpha_3
    ]

    start_urls = ["https://www.farmaciasunion.com/sucursales.json"]

    def parse(self, response):
        list_of_places = response.json()
        
        for place in list_of_places:
            coordinates = place.get("Coordenadas", "").split(", ")
            lat = coordinates[0] if len(coordinates) > 1 else ""
            lon = coordinates[1] if len(coordinates) > 1 else ""
            
            mappedAttributes = {
                'chain_name': self.brand_name,
                'chain_id': self.spider_chain_id,
                'ref': uuid.uuid4().hex,
                'addr_full': place.get("Direccion", ""),
                'city': place.get("Ciudad", ""),
                'street' : place.get("Calle",""),
                'state': place.get("Estado", ""),
                'phone': place.get("Numero", ""),
                'website': "https://www.farmaciasunion.com/sucursales.html",
                'lat': lat,
                'lon': lon,
            }

            yield GeojsonPointItem(**mappedAttributes)
