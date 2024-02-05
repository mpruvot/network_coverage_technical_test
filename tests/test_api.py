from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app
from custom_exceptions import AdressNotFoundError, DataNotFoundError
from models.coverage_model import NetworkCoverage

client = TestClient(app)


@patch("api.main.network_manager.retrieve_data_from_adress")
def test_get_network_coverage(mock_data):
    mock_data.return_value = NetworkCoverage(
        Orange={"2G": True, "3G": True, "4G": False},
        Bouygues={"2G": True, "3G": True, "4G": True},
        Sfr={"2G": True, "3G": True, "4G": False},
        Free=None,
    )
    response = client.get("/coverages/?q=Ouessant")
    assert response.status_code == 200
    assert response.json() == {
        "Orange": {"2G": True, "3G": True, "4G": False},
        "Bouygues": {"2G": True, "3G": True, "4G": True},
        "Sfr": {"2G": True, "3G": True, "4G": False},
        "Free": None,
    }
    assert mock_data.call_count == 1


def test_get_network_coverage_adress_not_found_error():
    with patch(
        "api.main.network_manager.retrieve_data_from_adress",
        side_effect=AdressNotFoundError("Address not found"),
    ):
        response = client.get("/coverages/?q=xxxxx")
        assert response.status_code == 404
        assert response.json() == {"detail": "Address not found"}


def test_get_network_coverage_data_not_found_error():
    with patch(
        "api.main.network_manager.retrieve_data_from_adress",
        side_effect=DataNotFoundError("Data not found for the provided address"),
    ):
        response = client.get("/coverages/?q=empty")
        assert response.status_code == 404
        assert response.json() == {"detail": "Data not found for the provided address"}


@patch("api.main.gps_to_adress")
def test_get_adress_from_gps(mock_data):
    mock_data.return_value = {
        "adress": "Ouessant",
        "city": "Ouessant",
    }
    response = client.get("/adresses/?lon=-5.0888561&lat=48.4565745")
    assert response.status_code == 200
    assert response.json() == {
        "adress": "Ouessant",
        "city": "Ouessant",
    }
    assert mock_data.call_count == 1
