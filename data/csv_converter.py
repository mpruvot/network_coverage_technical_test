import csv
import pathlib
import sys
from time import time

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import typer

from services.localisation_converters import lamber93_to_gps

app = typer.Typer()


@app.command()
def convert(source: str, dest: str) -> None:
    """
    Convert a CSV file with Lambert93 coordinates to a new file with GPS coordinates.

    Args:
        source (str): The path to the original CSV file.
        dest (str): The path to the converted CSV file.

    Returns:
        None
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


if __name__ == "__main__":
    app()
