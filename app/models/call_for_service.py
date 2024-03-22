from sqlalchemy import Column, Integer, Date, String, Boolean, Enum
from app.db import Base


class CallForService(Base):
    __tablename__ = "calls_for_service"
    __table_args__ = {"schema": "ssle_metro"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    year_month = Column(Date)
    year = Column(Integer)
    month = Column(String)
    fiscal_year = Column(String)
    transport_type = Column(String)
    line_name = Column(String)
    call_type = Column(String)
    station_name = Column(String)
    agency_name = Column(String)
    calls_count = Column(Integer)
    published = Column(Boolean)

    def __repr__(self):
        return f"CallForService({self.year_month}, {self.year}, {self.month}, {self.fiscal_year}, {self.transport_type}, {self.line_name}, {self.call_type}, {self.station_name}, {self.agency_name}, {self.calls_count}, {self.published})"

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
            "call_type": self.call_type,
            "station_name": self.station_name,
            "agency_name": self.agency_name,
            "calls_count": self.calls_count,
            "publish": self.published,
        }
