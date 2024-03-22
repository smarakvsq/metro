from sqlalchemy import Column, Integer, Date, String, Boolean, Enum
from app.db import Base


class Arrest(Base):
    __tablename__ = "arrest"
    __table_args__ = {"schema": "ssle_metro"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    year_month = Column(Date)
    year = Column(Integer)
    month = Column(String)
    fiscal_year = Column(String)
    transport_type = Column(String)
    line_name = Column(String)
    gender = Column(String)
    ethinicity = Column(String)
    station_name = Column(String)
    agency_name = Column(String)
    arrest_count = Column(Integer)
    published = Column(Boolean)

    def __repr__(self):
        return f"Arrest({self.year_month}, {self.year}, {self.month}, {self.fiscal_year}, {self.transport_type}, {self.line_name}, {self.gender}, {self.ethinicity}, {self.station_name}, {self.agency_name}, {self.arrest_count}, {self.published})"

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
            "gender": self.gender,
            "ethinicity": self.ethinicity,
            "station_name": self.station_name,
            "agency_name": self.agency_name,
            "arrest_count": self.arrest_count,
            "publish": self.published,
        }
