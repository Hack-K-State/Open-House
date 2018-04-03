import urllib2
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

url = "https://mlh.io/seasons/eu-2018/events"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
req = urllib2.Request(url, headers=hdr)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page, "html.parser")

names = []
cities = []
states = []

for elem in soup.findAll("h3", attrs={"itemprop": "name"}):
    hackathon_name = elem.text.encode('utf-8').strip()
    if hackathon_name != "Local Hack Day":
        names.append(hackathon_name)

for elem in soup.findAll("span", attrs={"itemprop": "addressLocality"}):
    hackathon_city = elem.text.encode('utf-8').strip()
    if hackathon_city != "Everywhere":
        cities.append(hackathon_city)

for elem in soup.findAll("span", attrs={"itemprop": "addressRegion"}):
    hackathon_state = elem.text.encode('utf-8').strip()
    if hackathon_state != "Worldwide":
        states.append(hackathon_state)

geolocator = Nominatim()
for i in range(len(names)):
    try:
        location = geolocator.geocode(cities[i] + ", " + states[i])
        print "var m" + str(i+155) + " = createMarker({lat: " + str(location.latitude) + ", lng: " + str(location.longitude) + "}, '" + names[i] + "');"
    except Exception, e:
        print str(e)
