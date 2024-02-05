import sys
from pathlib import Path
from unittest.mock import patch

import pytest
import requests
from pytest import approx

from custom_exceptions import AdressNotFoundError

sys.path.append(str(Path(__file__).parent.parent))

from services.localisation_converters import (
    adress_to_gps,
    gps_to_adress,
    gps_to_lamber93,
    lamber93_to_gps,
)


def test_lamber93_to_gps():
    x = 600000
    y = 200000
    expected_result = (-4.6047175834036524, 2.366062698352502)
    assert lamber93_to_gps(x, y) == approx(expected_result, rel=1e-9)


def test_gps_to_lamber93():
    lat = 48.8566
    long = 2.3522
    expected_result = (652469, 6862035)
    assert gps_to_lamber93(lat, long) == expected_result


@patch("requests.get")
def test_adress_to_gps(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "features": [
            {"geometry": {"coordinates": [-4.6047175834036524, 2.366062698352502]}}
        ]
    }
    adress = "Paris"
    expected_result = (2.366062698352502, -4.6047175834036524)
    assert adress_to_gps(adress) == expected_result


@patch("requests.get")
def test_adress_to_gps_not_found(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "features": [{"geometry": {"coordinates": []}}]
    }
    mock_get.side_effect = IndexError

    with pytest.raises(AdressNotFoundError):
        adress_to_gps("xxxxx")


@patch("requests.get")
def test_gps_to_adress(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "features": [
            {
                "properties": {
                    "label": "8 Boulevard du Port 80000 Amiens",
                    "city": "Amiens",
                }
            }
        ]
    }
    lon = "2.290084"
    lat = "49.897442"
    expected_result = {"adress": "8 Boulevard du Port 80000 Amiens", "city": "Amiens"}
    assert gps_to_adress(lon, lat) == expected_result
