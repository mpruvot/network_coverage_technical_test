import csv
from time import time

from services.localisation_converters import lamber93_to_gps


def csv_converter(
    source: str = "original_csv.csv", dest: str = "converted_csv.csv"
) -> None:
    """
    Convert a CSV file with Lambert93 coordinates to a new file with GPS coordinates.

    Args:
        source (str): The path to the original CSV file. Default is "original_csv.csv".
        dest (str): The path to the converted CSV file. Default is "converted_csv.csv".

    Returns:
        None

    Raises:
        ValueError: If the conversion of coordinates fails for a row, it is skipped.
    """
    with open(source, "r", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        with open(dest, "w", newline="") as newfile:
            writer = csv.writer(newfile, delimiter=";")
            headers = next(reader)
            writer.writerow(headers)

            time1 = time()
            for row in reader:
                try:
                    lat, long = lamber93_to_gps(int(row[1]), int(row[2]))
                    row[1], row[2] = lat, long
                    writer.writerow(row)
                except ValueError:
                    continue

            time2 = time()
            duration = time2 - time1

            print(f"Conversion done in {duration} seconds")
            # Done in 3.4 minutes


csv_converter()