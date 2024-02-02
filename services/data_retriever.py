import csv
import sys
from math import isclose
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from models.coverage_model import NetworkCoverage
from services.localisation_converters import adress_to_gps


class DataRetrieverService:
    """
    DataRetrieverService class, used to retrieve and convert data from the 'converted_csv.csv' file.
    """

    def __init__(self) -> None:
        pass

    def _retrieve_data_from_coordinates(self, lat: float, long: float) -> list:
        """
        Retrieve data from coordinates.

        Args:
            lat (float): The latitude coordinate.
            long (float): The longitude coordinate.

        Returns:
            list: A list of matching rows from the data.

        """
        matching_rows = []
        with open("converted_csv.csv", newline="") as f:
            reader = csv.reader(f, delimiter=";")

            next(reader)

            for row in reader:
                try:
                    x = float(row[1])
                    y = float(row[2])
                    if isclose(lat, x, abs_tol=0.001) and isclose(
                        long, y, abs_tol=0.001
                    ):
                        matching_rows.append(row)
                except ValueError:
                    continue

        return matching_rows

    def _format_rows_to_network_coverage(self, rows: list) -> NetworkCoverage:
        """
        Formats the rows of data into a NetworkCoverage object.

        Args:
            rows (list): A list of rows containing network coverage data.

        Returns:
            NetworkCoverage: An instance of the NetworkCoverage class representing the formatted network coverage data.
        """
        provider_code = {
            "20801": "Orange",
            "20810": "Sfr",
            "20820": "Bouygues",
            "20815": "Free",
        }

        coverage_data = {}

        for row in rows:
            operator = provider_code.get(row[0])
            if operator:
                coverage_data[operator.capitalize()] = {
                    "2G": bool(int(row[3])),
                    "3G": bool(int(row[4])),
                    "4G": bool(int(row[5])),
                }

        return NetworkCoverage(**coverage_data)

    def retrieve_data_from_adress(self, adress: str) -> NetworkCoverage:
        """
        Retrieves network coverage data based on the given address.

        Args:
            adress (str): The address to retrieve data for.

        Returns:
            NetworkCoverage: The network coverage data for the given address.
        """
        adress_coordinates = adress_to_gps(adress)
        data_from_coordinates = self._retrieve_data_from_coordinates(
            *adress_coordinates
        )
        network_coverage = self._format_rows_to_network_coverage(data_from_coordinates)
        return network_coverage


service = DataRetrieverService()
