from sqlalchemy import Column, Integer, Float, String
from app.db import Base


class Location(Base):
    __tablename__ = "location"
    __table_args__ = {"schema": "ssle_metro"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    transport_type = Column(String)
    station_name = Column(String)
    line_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    def __repr__(self):
        return f"Location({self.transport_type}, {self.station_name}, {self.line_name}, {self.latitude}, {self.longitude})"

    def __str__(self):
        return self.__repr__()

    def to_json(self):
        return {
            "transport_type": self.transport_type,
            "station_name": self.station_name,
            "line_name": self.line_name,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
