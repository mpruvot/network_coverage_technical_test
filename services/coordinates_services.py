import json

import requests
from pyproj import Transformer


def lamber93_to_gps(x: int, y: int) -> tuple:
    """Convert Lambert 93 coordinates to GPS coordinates (longitude, latitude)"""

    transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326")
    long, lat = transformer.transform(x, y)

    return long, lat


def gps_to_lamber93(lat: float, long: float) -> tuple:
    """Convert GPS coordinates (latitude, longitude) to Lambert93 coordinates and round to integers"""
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154")
    x, y = transformer.transform(long, lat)

    return int(round(x)), int(round(y))


def adress_to_gps(adress: str) -> tuple:
    """Convert adress to GPS coordinates (longitude, latitude)"""
    API_URL = "https://api-adresse.data.gouv.fr/search/"

    try:
        response = requests.get(
            API_URL,
            params={
                "q": adress,
                "limit": 1,
                "autocomplete": 0,
            },
        )
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=4))
        long = data["features"][0]["geometry"]["coordinates"][0]
        lat = data["features"][0]["geometry"]["coordinates"][1]
        return lat, long

    except requests.exceptions.HTTPError as err:
        raise requests.exceptions.HTTPError(err)

    except IndexError as err:
        raise IndexError(err)


print(adress_to_gps("17,rue du delta 75009 paris"))
