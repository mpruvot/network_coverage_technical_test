import csv
from time import time

from services.localisation_converters import lamber93_to_gps


def csv_converter(
    source: str = "original_csv.csv", dest: str = "converted_csv.csv"
) -> None:
    """Given the Orginal csv with lamber93 coordinates, this function create a new file with Gps coordinates instead"""
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
