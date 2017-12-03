from urllib.request import urlopen
from bs4 import BeautifulSoup
from pick import pick
from pprint import pprint
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json

allstops_hashtable = {}
buschtable = {}
livitable = {}
cactable = {}
cdtable = {}
othertable = {}

def set_stopIDS():
    '''Create a dictionary of all stops, their ids, and their long, lat. If a stop does not have an id it is not included.'''
    global allstops_hashtable
    find_stopid = 'http://webservices.nextbus.com/service/publicJSONFeed?a=rutgers&command=routeConfig'
    page = urlopen(find_stopid)
    json_page = json.load(page)

    for route in json_page['route']:
        for stop in route['stop']:
            try:
                #if stop['stopId'] not in allstops_hashtable:
                stopid = stop['stopId']
                coordinate = (float(stop['lat']), float(stop['lon']))
                allstops_hashtable[stop['title']] = [stopid, coordinate]
            except:
                continue

def define_campuses():
    '''Attempts to breakup stops to different dictionaries based off of campus'''
    global allstops_hashtable
    global buschtable
    global livitable
    global cactable
    global cdtable
    global othertable

    #each of these polygons was created using: https://multiplottr.com
    busch = Polygon([(40.521760, -74.488335), (40.511907, -74.459667), (40.525217, -74.452543), (40.528936, -74.467564)])
    livingston = Polygon([(40.524174, -74.446020), (40.517339, -74.431193), (40.523815, -74.427953), (40.530763, -74.440956)])
    collegeave = Polygon([(40.499116, -74.462543), (40.492328, -74.446235), (40.499801, -74.438381), (40.508350, -74.453144)])
    cookdoug = Polygon([(40.478521, -74.453616), (40.466376, -74.425120), (40.480251, -74.414349), (40.490826, -74.440227)])

    busch_list = []
    livi_list = []
    collegeave_list = []
    cookdoug_list = []
    other_list = []

    for key, value in allstops_hashtable.items():
        if busch.contains(Point(value[1])):
            busch_list.append(key)
        elif livingston.contains(Point(value[1])):
            livi_list.append(key)
        elif collegeave.contains(Point(value[1])):
            collegeave_list.append(key)
        elif cookdoug.contains(Point(value[1])):
            cookdoug_list.append(key)
        else: other_list.append(key)


    buschtable = {k: allstops_hashtable[k] for k in busch_list}
    livitable = {k: allstops_hashtable[k] for k in livi_list}
    cactable = {k: allstops_hashtable[k] for k in collegeave_list}
    cdtable = {k: allstops_hashtable[k] for k in cookdoug_list}
    othertable = {k: allstops_hashtable[k] for k in other_list}


def display_campus_stops(campus):

    if campus == 'Busch':
        title = 'Busch Bus Stops'
        options = list(buschtable.keys())
        options.sort()
        option, index = pick(options, title)
        return_all_buses_for_stop(option)
    elif campus == 'Livingston':
        title = 'Livi Bus Stops'
        options = list(livitable.keys())
        options.sort()
        option, index = pick(options, title)
        return_all_buses_for_stop(option)
    elif campus == 'College Ave':
        title = 'College Ave Bus Stops'
        options = list(cactable.keys())
        options.sort()
        option, index = pick(options, title)
        return_all_buses_for_stop(option)
    elif campus == 'C/D':
        title = 'Cook Doug Stops'
        options = list(cdtable.keys())
        options.sort()
        option, index = pick(options, title)
        return_all_buses_for_stop(option)
    else:
        title = 'Other Stops'
        options = list(othertable.keys())
        options.sort()
        option, index = pick(options, title)
        return_all_buses_for_stop(option)

def return_all_buses_for_stop(stopname):
    global allstops_hashtable
    general_url = 'http://webservices.nextbus.com/service/publicJSONFeed?a=rutgers&command=predictions&stopId={}'

    stop = allstops_hashtable.get(stopname)
    stopid = stop[0]

    page = urlopen(general_url.format(stopid))
    json_page = json.load(page)

    print("Predictions for {} are as follows: ".format(stopname))
    for route in json_page['predictions']:
        try:
            route['direction']
            print()
            print("============{}===========".format(route['routeTitle']))
            for active_routes in route['direction']['prediction']:
                print("vehicle number {} is going to be there in {} miutes".format(active_routes['vehicle'], active_routes['minutes']))
        except:
            print("============{}===========".format(route['routeTitle']))
            print("No predictions")
            continue

def main():
    global allstops_hashtable
    set_stopIDS()
    define_campuses()

    title = 'Please choose the campus you are interested in:'
    options = ('Busch', 'Livingston', 'College Ave', 'C/D', 'Other (unable to map these stops)')
    option, index = pick(options, title)

    display_campus_stops(option)

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
