import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import requests
from pyproj import Transformer

from custom_exceptions import AdressNotFoundError


def lamber93_to_gps(y: int, x: int) -> tuple:
    """Convert Lambert 93 coordinates to GPS coordinates (longitude, latitude)"""

    transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326")
    lat, long = transformer.transform(y, x)

    return lat, long


def gps_to_lamber93(lat: float, long: float) -> tuple:
    """Convert GPS coordinates (latitude, longitude) to Lambert93 coordinates and round to integers"""
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154")
    x, y = transformer.transform(lat, long)

    return int(round(x)), int(round(y))


def adress_to_gps(adress: str) -> tuple:
    """Converts an address to GPS coordinates.

    Args:
        adress (str): The address to convert.

    Returns:
        tuple: A tuple containing the latitude and longitude coordinates.

    Raises:
        AdressNotFoundError: If no data is found for the given address.
    """
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
        # The api returns Long/Lat -> y/x
        long = data["features"][0]["geometry"]["coordinates"][0]
        lat = data["features"][0]["geometry"]["coordinates"][1]
        return lat, long

    except requests.exceptions.HTTPError as err:
        raise AdressNotFoundError("No data found for this adress: " + str(err))

    except IndexError as err:
        raise AdressNotFoundError("No data found for this adress: " + str(err))


print(adress_to_gps("17, rue du delta"))
