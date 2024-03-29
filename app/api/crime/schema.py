from pydantic import BaseModel
from typing import Optional, List


class CrimeSchema(BaseModel):
    line_name: Optional[str]
    transport_type: Optional[str]
    dates: List[str]
    severity: str
    crime_category: Optional[str]
    vetted: bool
    published: bool
    graph_type: str
