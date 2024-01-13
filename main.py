import geocoder
import requests

g = geocoder.ip('me')

print(g.city)
print(g.latlng)