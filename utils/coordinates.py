import googlemaps
from bot.models import Place


class Coordinates:
    """
    Get lat,lng of a place through its address
    """
    def __init__(self):
        self.k = 'AIzaSyAftwrvS2Mphv821bXwZMOR3EmC6esH8Fk'

    def get_coords(self, places):
        gmaps = googlemaps.Client(key = self.k)
        for place in places:
            try:
                coords = gmaps.geocode(place.address)
                lat = coords[0]['geometry']['location']['lat']
                lng = coords[0]['geometry']['location']['lng']
                print("{}. {}'s coords are lat: {}, lng: {}".format(place.id, place.name, lat, lng))

                place_object = Place.objects.get(id=place.id)
                place_object.lat = lat
                place_object.lng = lng
                place_object.save()
            except:
                print('something went wrong with {}'.format(place.name))