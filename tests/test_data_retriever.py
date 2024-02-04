from unittest.mock import patch

import pytest

from custom_exceptions import DataNotFoundError
from models.coverage_model import NetworkCoverage
from services.data_retriever import DataRetrieverService


@pytest.fixture
def data_retriever():
    return DataRetrieverService()


def test__retrieve_data_from_coordinates(data_retriever):
    # matching row found
    lat = 48.858844
    long = 2.294350
    assert len(data_retriever._retrieve_data_from_coordinates(lat, long)) > 0

    # No matching row found
    lat = 0.0
    long = 0.0
    assert len(data_retriever._retrieve_data_from_coordinates(lat, long)) == 0


def test__format_rows_to_network_coverage(data_retriever):

    # Valid rows
    rows = [
        ["20801", "48.858844", "2.294350", "1", "1", "1"],
        ["20810", "48.858844", "2.294350", "0", "1", "1"],
    ]
    network_coverage = data_retriever._format_rows_to_network_coverage(rows)
    assert network_coverage.Orange.get("2G") == True
    assert network_coverage.Sfr.get("3G") == True

    # Invalid rows
    rows = [
        ["20801", "48.858844", "2.294350", "1", "1", "1"],
        ["20810", "48.858844", "2.294350", "0", "1", "xxxxxxxxx"],
    ]
    network_coverage = data_retriever._format_rows_to_network_coverage(rows)
    assert network_coverage.Orange.get("2G") == True
    assert network_coverage.Sfr.get("3G") == False
