import requests
import geograpy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

api_key = "YOUR_API_KEY"
final = []
geolocator = Nominatim(user_agent="newsonmap")
app = Flask(__name__, template_folder=".")
GoogleMaps(app)


def do_geocode(address):
    try:
        return geolocator.geocode(address, timeout=10)
    except GeocoderTimedOut:
        return do_geocode(address)


@app.before_first_request
def do_something_only_once():
    source_url = "https://newsapi.org/v2/sources?language=en&apiKey=" + api_key
    #source_req = requests.get(source_url).json()
    #source_list = source_req["sources"]
    source_list = ['abc-news','bbc-news','bbc-sport','business-insider','cnbc','cnn','google-news','techcrunch','the-hindu','the-times-of-india']
    description = []
    title = []
    url = []
    urlimg=[]
    ans = []

    for sr in source_list:
        main_url = "https://newsapi.org/v2/top-headlines?sources=" + sr + "&apiKey=" + api_key
        print(main_url)
        open_bbc_page = requests.get(main_url).json()
        article = open_bbc_page["articles"]

        for ar in article:
            url.append(ar["url"])
            if (ar["title"] == None or ar["title"] == ""):
                title.append("NULL")
            else:
                title.append(ar["title"])

            if (ar["description"] == None or ar["description"] == ""):
                description.append("NULL")
            else:
                description.append(ar["description"])

            urlimg.append((ar["urlToImage"]))

    for i in range(len(title)):
        # print(title[i] + " #### " + url[i] + " ##### " + description[i]+" ### ")
        # if (title[i] != None and description[i] != None and title[i] != "" and description[i] != ""):
        place1 = geograpy.get_place_context(text=title[i])
        place2 = geograpy.get_place_context(text=description[i])
        # print(places.cities)
        # print(places.countries)
        ans.append(place1.cities + place1.countries + place2.cities + place2.countries)
        ans[i] = list(set(ans[i]))
        # print(ans[i])
        # pl=GeoText(results[i])
        # print(str(pl.cities))

    for i in range(len(title)):
        A = title[i]
        B = url[i]
        F=urlimg[i]
        C = ans[i]
        for n in C:
            location = do_geocode(n)
            if (location != None):
                D = location.latitude
                E = location.longitude
                final.append([A, B, D, E,F])
                print([A, B, D, E,F])

    #for i in final:
    #   print(i)

    print('NLP PART DONE')


@app.route("/")
def mapview():
    # creating a map in the view

    mark1 = []

    for i in final:
        ndic = {
            'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
            'lat': i[2],
            'lng': i[3],
            'infobox': "<b>" + i[0] + "</b><a href='"+i[1]+"'><img src='"+i[4]+"' height=100px;width=80px; /></a>"
        }

        mark1.append(ndic)

    sndmap = Map(
        identifier="sndmap",
        lat=13.009479,
        lng=80.235089,
        zoom=3,
        style="height:100vh;width:100vw;margin:0;",
        markers=mark1
    )
    return render_template('example.html', sndmap=sndmap)


if __name__ == "__main__":
    app.run(debug=True)
