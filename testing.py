from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from pprint import pprint

quote_page = 'http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers&command=vehicleLocations'
json_url = 'http://webservices.nextbus.com/service/publicJSONFeed?a=rutgers&command=vehicleLocations'
page = urlopen(json_url)
# soup = BeautifulSoup(page, 'lxml')
# test = soup.find_all('vehicle')


data = json.load(page)


for vehicle in data['vehicle']:
    print(vehicle['dirTag'])


# name_box = soup.find('h1', attrs={'class': 'name'})
# name = name_box.text.strip()
# print name
#
# price_box = soup.find('div', attrs={'class':'price'})
# price = price_box.text
# print price
