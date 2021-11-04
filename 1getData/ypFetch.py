import time

import requests
import csv
from bs4 import BeautifulSoup

placeHolder = []

states = ["MA", "NH", "CT", "IL", "MI", "CA", "TX", "FL", "NC", "VA", "MD"]

for place in states:
    urls = ["https://www.yellowpages.com/search?search_terms={}&geo_location_terms={}&page={}".format("Software",
                                                                                                      place, page) for page in range(1, 10)]
    for url in urls:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "lxml")

        def get_text(item: object, path: object) -> object:
            return item.select_one(path).text if item.select_one(path) else ""

        for item in soup.select(".info"):
            d = {'name': get_text(item, "a.business-name span"), 'streetAddress': get_text(item, ".street-address"),
                 'addressLocality': get_text(item, ".locality"), 'addressRegion': get_text(item, ".locality + span"),
                 'postalCode': get_text(item, ".locality + span + span"), 'phone': get_text(item, ".phones")}
            try:
                d['web'] = item.find("a", {"class": "track-visit-website"})["href"]
            except:
                pass
            placeHolder.append(d)
    time.sleep(1)

with open(r'yp.csv', "w", newline="") as infile:
    writer = csv.DictWriter(infile,
                            ['name', 'streetAddress', 'addressLocality', 'addressRegion', 'postalCode', 'phone', 'web'])
    writer.writeheader()
    for elem in placeHolder:
        writer.writerow(elem)

