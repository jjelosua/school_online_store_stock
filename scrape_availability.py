#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import re
import json
import requests
from bs4 import BeautifulSoup
import datetime
from time import sleep


CLOTHES = [
    {"url": "https://jesuitasasvigo.latiendaruisell.com/producto/babero-azul/",
    "talla": "2",
    "descripcion": "mandilon T2: "},
    {"url": "https://jesuitasasvigo.latiendaruisell.com/producto/bermuda-deportiva-t0-t8/",
    "talla": "2",
    "descripcion": "bermuda deportiva T2: "},
    {"url": "https://jesuitasasvigo.latiendaruisell.com/producto/camiseta-manga-corta-t0-t8/",
    "talla": "2",
    "descripcion": "camiseta manga corta T2: "},
    {"url": "https://jesuitasasvigo.latiendaruisell.com/producto/camiseta-manga-corta-t0-t8/",
    "talla": "6",
    "descripcion": "camiseta manga corta T6: "},
    {"url": "https://jesuitasasvigo.latiendaruisell.com/producto/chaqueta-de-chandal/",
    "talla": "6",
    "descripcion": "Chaqueta chandal T6: "},
    {"url": "https://jesuitasasvigo.latiendaruisell.com/producto/polo-manga-corta/",
    "talla": "6",
    "descripcion": "Polo manga corta T6: "},
    {"url": "https://jesuitasasvigo.latiendaruisell.com/producto/chaqueta-de-chandal/",
    "talla": "8",
    "descripcion": "Chanqueta semicisne T8: "}]

cwd = os.path.dirname(__file__)

try:
    session = requests.Session()
    msg = "Disponibilidad:"
    found_stock = False
    for d in CLOTHES:
        r = session.get(d['url'])
        soup = BeautifulSoup(r.content, 'html.parser')
        aux = soup.find('form', id='nm-variations-form')
        variations = json.loads(aux['data-product_variations'])
        #print(type(variations))
        #print("size: %s" % (len(variations)))
        for v in variations:
            if (v['attributes']['attribute_pa_talla'] == d['talla']):
                # print('encontrada talla: %s' % (v['attributes']['attribute_pa_talla']))
                stock = BeautifulSoup(v['availability_html'].strip('\n'), 'html.parser')
                msg += " %s %s |" % (d['descripcion'], stock.find('p').string)
                if (stock.find('p').string != "Agotado"):
                    found_stock = True
    
    if found_stock:
        print(1)
    else:
        print(0)
    
    env_file = os.getenv('GITHUB_ENV')
    with open(env_file, "a") as myfile:
        myfile.write("STOCK=%s" % (msg))
except Exception as e:
    print("could not retrieve stock data")
    raise e