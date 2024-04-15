from typing import List, Optional

from pydantic import BaseModel


class CrimeSchema(BaseModel):
    line_name: Optional[str]
    transport_type: Optional[str]
    dates: List[str]
    severity: str
    crime_category: Optional[str]
    vetted: bool
    published: bool
    graph_type: str
