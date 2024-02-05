from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from custom_exceptions import AdressNotFoundError, DataNotFoundError
from models.coverage_model import NetworkCoverage
from services.data_retriever import DataRetrieverService
from services.localisation_converters import gps_to_adress

app = FastAPI()

network_manager = DataRetrieverService()


@app.get("/")
def redirect_to_docs():
    """automatically redirect to docs when accessing root"""
    return RedirectResponse(url="/docs/")


@app.get("/coverages/", response_model=NetworkCoverage)
def get_network_coverage(q: str) -> NetworkCoverage:
    """Retrieve network coverage data based on the given address."""
    try:
        return network_manager.retrieve_data_from_adress(q)
    except AdressNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    except DataNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@app.get("/adresses/", response_model=dict)
def get_adress_from_gps(lon: str, lat: str) -> dict:
    """Retrieve adress/Location from gps coordinates"""
    try:
        return gps_to_adress(lat=lat, long=lon)

    except AdressNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    except DataNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
