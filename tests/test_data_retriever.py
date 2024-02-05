from unittest.mock import patch

import pytest

from custom_exceptions import DataNotFoundError
from models.coverage_model import NetworkCoverage
from services.data_retriever import DataRetrieverService
from services.localisation_converters import adress_to_gps


def test_retrieve_data_from_coordinates():
    data_retriever = DataRetrieverService()
    matching_row = [
        ["20801", "48.456574558829914", "-5.0888561153013425", "1", "1", "0"],
        ["20810", "48.46285384829354", "-5.088018169414727", "1", "1", "0"],
        ["20820", "48.462881615228916", "-5.088008862939317", "1", "1", "1"],
    ]
    assert (
        data_retriever._retrieve_data_from_coordinates(48.4565745588, -5.088856115)
        == matching_row
    )


def test_format_rows_to_network_coverage():
    data_retriever = DataRetrieverService()
    rows = [
        ["20801", "48.456574558829914", "-5.0888561153013425", "1", "1", "0"],
        ["20810", "48.46285384829354", "-5.088018169414727", "1", "1", "0"],
        ["20820", "48.462881615228916", "-5.088008862939317", "1", "1", "1"],
    ]

    response = NetworkCoverage(
        Orange={"2G": True, "3G": True, "4G": False},
        Bouygues={"2G": True, "3G": True, "4G": True},
        Sfr={"2G": True, "3G": True, "4G": False},
        Free=None,
    )
    assert isinstance(
        data_retriever._format_rows_to_network_coverage(rows), NetworkCoverage
    )

    assert data_retriever._format_rows_to_network_coverage(rows) == response


@patch("services.data_retriever.adress_to_gps")
def test_retrieve_data_from_adress(mock_adress_to_gps):
    data_retriever = DataRetrieverService()
    mock_adress_to_gps.return_value = (48.4565745, -5.0888561)
    expected_network_coverage = NetworkCoverage(
        Orange={"2G": True, "3G": True, "4G": False},
        Bouygues={"2G": True, "3G": True, "4G": True},
        Sfr={"2G": True, "3G": True, "4G": False},
        Free=None,
    )

    result = data_retriever.retrieve_data_from_adress("Ouessant")

    assert isinstance(result, NetworkCoverage)
    assert result == expected_network_coverage
