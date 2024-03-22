from sqlalchemy import Column, Integer, Date, String, Boolean
from app.db import Base


class CrimeVetted(Base):
    __tablename__ = "crime_vetted"
    __table_args__ = {"schema": "ssle_metro"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    year_month = Column(Date)
    year = Column(Integer)
    month = Column(String)
    fiscal_year = Column(String)
    transport_type = Column(String)
    line_name = Column(String)
    severity = Column(String)
    ucr = Column(String)
    crime_name = Column(String)
    station_name = Column(String)
    agency_name = Column(String)
    crime_count = Column(Integer)
    published = Column(Boolean, default=False)

    def __repr__(self):
        return f"CrimeVetted({self.year_month}, {self.year}, {self.month}, {self.fiscal_year}, {self.transport_type}, {self.line_name}, {self.severity}, {self.ucr}, {self.crime_name}, {self.station_name}, {self.agency_name}, {self.crime_count}, {self.published})"

    def __str__(self):
        return self.__repr__()

    def to_json(self):
        return {
            "year_month": str(self.year_month),
            "year": self.year,
            "month": self.month,
            "fiscal_year": self.fiscal_year,
            "transport_type": self.transport_type,
            "line_name": self.line_name,
            "severity": self.severity,
            "ucr": self.ucr,
            "crime_name": self.crime_name,
            "station_name": self.station_name,
            "agency_name": self.agency_name,
            "crime_count": self.crime_count,
            "published": self.published,
        }
