from urllib.request import urlopen
from bs4 import BeautifulSoup

quote_page = 'http://webservices.nextbus.com/service/publicXMLFeed?a=rutgers&command=vehicleLocations'
page = urlopen(quote_page)
soup = BeautifulSoup(page, 'lxml')

test = soup.find_all('vehicle')

for t in test:
    print(t)


# name_box = soup.find('h1', attrs={'class': 'name'})
# name = name_box.text.strip()
# print name
#
# price_box = soup.find('div', attrs={'class':'price'})
# price = price_box.text
# print price
