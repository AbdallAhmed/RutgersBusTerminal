import urllib2
from bs4 import BeautifulSoup

quote_page = 'http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers&command=vehicleLocations'
page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, 'lxml')

test = soup.find('vehicle')
print test['dirtag']

# name_box = soup.find('h1', attrs={'class': 'name'})
# name = name_box.text.strip()
# print name
#
# price_box = soup.find('div', attrs={'class':'price'})
# price = price_box.text
# print price
