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

    #This is the URL we are requesting. As according to the nextbusAPI if we add the &terse we half the amount of data coming back
    find_stopid = 'http://webservices.nextbus.com/service/publicJSONFeed?a=rutgers&command=routeConfig&terse'
    page = urlopen(find_stopid)
    json_page = json.load(page)


    for route in json_page['route']:
        for stop in route['stop']:
            #not all stops have an ID so we are going to try and see if the stopid exists
            try:
                stopid = stop['stopId']

                #This becomes confusing as a stop can have multiple IDs

                if stop['title'] not in list(allstops_hashtable.keys()):
                    coordinate = (float(stop['lat']), float(stop['lon']))
                    #We are adding the stopid in as a list so that we can make room for multiples
                    allstops_hashtable[stop['title']] = [[stopid], coordinate]
                elif stop['title'] in list(allstops_hashtable.keys()) and stopid not in allstops_hashtable[stop['title']][0]:
                    #if we have the stop but do not have the stopid we have to add it
                    allstops_hashtable[stop['title']][0].append(stopid)
            except:
                continue

def define_campuses():
    '''Attempts to breakup stops to different dictionaries based off of campus.
    Instead of just hardcoding the campuses we attempt to split it up goegraphically.
    This is just in case there are new bus stops added so they automatically gropu to the appropriate campus'''
    global allstops_hashtable
    global buschtable
    global livitable
    global cactable
    global cdtable
    global othertable

    #Each of these polygons was created using: https://multiplottr.com
    busch = Polygon([(40.521760, -74.488335), (40.511907, -74.459667), (40.525217, -74.452543), (40.528936, -74.467564)])
    livingston = Polygon([(40.524174, -74.446020), (40.517339, -74.431193), (40.523815, -74.427953), (40.530763, -74.440956)])
    collegeave = Polygon([(40.499116, -74.462543), (40.492328, -74.446235), (40.499801, -74.438381), (40.508350, -74.453144)])
    cookdoug = Polygon([(40.478521, -74.453616), (40.466376, -74.425120), (40.480251, -74.414349), (40.490826, -74.440227)])

    #Temp list that will be used for list logic later on
    busch_list = []
    livi_list = []
    collegeave_list = []
    cookdoug_list = []
    other_list = []

    #Every stop has a point that is mapped to it and then
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
    '''Handles displaying the different stops for each campus'''
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
    '''Takes the stop name and then gets predictions for the stop'''
    global allstops_hashtable
    general_url = 'http://webservices.nextbus.com/service/publicJSONFeed?a=rutgers&command=predictions&stopId={}'

    stop = allstops_hashtable.get(stopname)
    stopids = stop[0]

    print("Predictions for {} are as follows: ".format(stopname))
    for stopid in stopids:
        page = urlopen(general_url.format(stopid))
        json_page = json.load(page)

        if isinstance(json_page['predictions'], list):
            for route in json_page['predictions']:
                try:
                    route['direction']
                    print()
                    print("============{}===========".format(route['routeTitle']))
                    for active_routes in route['direction']['prediction']:
                        print("vehicle number {} is going to be there in {} miutes".format(active_routes['vehicle'], active_routes['minutes']))
                except:
                    continue
        else:
            try:
                fullvar = json_page['predictions']
                print()
                print("============{}===========".format(fullvar['routeTitle']))
                for active_routes in fullvar['direction']['prediction']:
                    print("vehicle number {} is going to be there in {} miutes".format(active_routes['vehicle'], active_routes['minutes']))
            except:
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
