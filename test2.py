import requests
import geograpy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

api_key="5fe8b03a190141f2a7b9b336b6ae526a"
final=[]
geolocator = Nominatim(user_agent="newsonmap")


def do_geocode(address):
    try:
        return geolocator.geocode(address, timeout=10)
    except GeocoderTimedOut:
        return do_geocode(address)

def News():

    source_url="https://newsapi.org/v2/sources?language=en&apiKey="+api_key
    source_req=requests.get(source_url).json()
    source_list=source_req["sources"]
    description = []
    title = []
    url=[]
    ans = []

    for sr in source_list:
        main_url = "https://newsapi.org/v2/top-headlines?sources="+sr["id"]+"&apiKey="+api_key
        print(main_url)
        open_bbc_page = requests.get(main_url).json()
        article = open_bbc_page["articles"]

        for ar in article:
            url.append(ar["url"])
            if(ar["title"]==None or ar["title"]==""):
                title.append("NULL")
            else:
                title.append(ar["title"])

            if (ar["description"] == None or ar["description"]==""):
                description.append("NULL")
            else:
                description.append(ar["description"])

    for i in range(len(title)):
        #print(title[i] + " #### " + url[i] + " ##### " + description[i]+" ### ")
        #if (title[i] != None and description[i] != None and title[i] != "" and description[i] != ""):
        place1=geograpy.get_place_context(text=title[i])
        place2 = geograpy.get_place_context(text=description[i])
        #print(places.cities)
        #print(places.countries)
        ans.append(place1.cities + place1.countries + place2.cities + place2.countries)
        ans[i]=list(set(ans[i]))
        #print(ans[i])
        #pl=GeoText(results[i])
        #print(str(pl.cities))

    for i in range(len(title)):
        A=title[i]
        B=url[i]
        C=ans[i]
        for n in C:
            location =do_geocode(n)
            if(location != None):
                D=location.latitude
                E=location.longitude
                final.append([A,B,D,E])

    for i in final:
        print(i)





if __name__ == '__main__':
    News()