from typing import Dict, Optional

from pydantic import BaseModel, Field


class NetworkCoverage(BaseModel):
    """Network coverage model, representing the network coverage of the 4 main French operator"""

    Orange: Optional[Dict] = Field(None, description="Orange network coverage")
    Bouygues: Optional[Dict] = Field(None, description="Bouygues network coverage")
    Sfr: Optional[Dict] = Field(None, description="SFR network coverage")
    Free: Optional[Dict] = Field(None, description="Free network coverage")
