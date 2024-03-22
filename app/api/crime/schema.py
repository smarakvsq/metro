from pydantic import BaseModel
from typing import Optional


class CrimeDetails(BaseModel):
    route: str
    transport_type: str
    from_date: str
    to_date: str
    crime_type: str
    crime_category: str
