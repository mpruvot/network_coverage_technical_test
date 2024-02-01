import requests
from pyproj import Transformer


def lamber93_to_gps(x: int, y: int) -> tuple:
    """Convert Lambert 93 coordinates to GPS coordinates (longitude, latitude)"""

    transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326")
    long, lat = transformer.transform(x, y)

    return long, lat


def gps_to_lamber93(long: float, lat: float) -> tuple:
    """Convert GPS coordinates (longitude, latitude) to Lambert 93 coordinates"""

    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154")
    x, y = transformer.transform(long, lat)

    return x, y


def adress_to_gps(adress: str) -> tuple:
    """Convert adress to GPS coordinates (longitude, latitude)"""
    api_url = "https://api-adresse.data.gouv.fr/search/?q="

    try:
        response = requests.get(api_url + adress)
        response.raise_for_status()
        response_json = response.json()
        long = response_json["features"][0]["geometry"]["coordinates"][0]
        lat = response_json["features"][0]["geometry"]["coordinates"][1]

        return long, lat

    except requests.exceptions.HTTPError as err:
        raise requests.exceptions.HTTPError(err)

    except IndexError as err:
        raise IndexError(err)
