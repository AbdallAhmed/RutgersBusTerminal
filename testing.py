from urllib.request import urlopen
from bs4 import BeautifulSoup
from pick import pick
import json
from pprint import pprint

allstops_hashtable = {}

def set_stopIDS( stopname ):
    global allstops_hashtable
    find_stopid = 'http://webservices.nextbus.com/service/publicJSONFeed?a=rutgers&command=routeConfig'
    page = urlopen(find_stopid)

    json_page = json.load(page)

    # stopname_stopid_hashtable = {}

    for route in json_page['route']:
        for stop in route['stop']:
            try:
                if stop['stopId'] not in allstops_hashtable:
                    allstops_hashtable[stop['title']] = stop['stopId']
            except:
                continue

def main():
    global allstops_hashtable
    set_stopIDS("test")
    title = 'Please choose the bus stop you want predictions for:'
    options = list(allstops_hashtable)
    option, index = pick(options, title)

if __name__ == "__main__":
    main()

# quote_page = 'http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers&command=vehicleLocations'
# json_url = 'http://webservices.nextbus.com/service/publicJSONFeed?a=rutgers&command=vehicleLocations'
#
# test_url = 'http://webservices.nextbus.com/service/publicJSONFeed?a=rutgers&command=predictions&stopId=1029'
# page = urlopen(test_url)
# # soup = BeautifulSoup(page, 'lxml')
# # test = soup.find_all('vehicle')
#
#
# data = json.load(page)
# pprint(data)

# for vehicle in data['vehicle']:
#     print(vehicle['routeTag'] + " " + vehicle['speedKmHr'])


# name_box = soup.find('h1', attrs={'class': 'name'})
# name = name_box.text.strip()
# print name
#
# price_box = soup.find('div', attrs={'class':'price'})
# price = price_box.text
# print price
