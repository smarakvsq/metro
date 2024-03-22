from sqlalchemy import Column, Integer, Date, String, Boolean, Enum
from app.db import Base


class CrimeUnvetted(Base):
    __tablename__ = "crime_unvetted"
    __table_args__ = {"schema": "ssle_metro"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    year_month = Column(Date)
    year = Column(Integer)
    month = Column(String)
    fiscal_year = Column(String)
    week_no = Column(Integer)
    from_date = Column(Date)  # clarify
    to_date = Column(Date)  # clarify
    transport_type = Column(String)  # [Rail, Bus]
    line_name = Column(String)
    severity = Column(String)  # rename to severeity
    ucr = Column(String)  # crime cat [Property, person, society]
    crime_name = Column(String)
    station_name = Column(String)
    agency_name = Column(String)  # [LAPD, LASD, LBPD]
    crime_count = Column(Integer)
    published = Column(Boolean, default=False)

    def __repr__(self):
        return f"CrimeUnvetted({self.year_month}, {self.year}, {self.month}, {self.fiscal_year}, {self.week_no}, {self.from_date}, {self.to_date}, {self.transport_type}, {self.line_name}, {self.severity}, {self.ucr}, {self.crime_name}, {self.station_name}, {self.agency_name}, {self.crime_count}, {self.published})"

    def __str__(self):
        return self.__repr__()

    def to_json(self):
        return {
            "year_month": str(self.year_month),
            "year": self.year,
            "month": self.month,
            "fiscal_year": self.fiscal_year,
            "week_no": self.week_no,
            "from_date": str(self.from_date),
            "to_date": str(self.to_date),
            "transport_type": self.transport_type,
            "line_name": self.line_name,
            "severity": self.severity,
            "ucr": self.ucr,
            "crime_name": self.crime_name,
            "station_name": self.station_name,
            "agency_name": self.agency_name,
            "crime_count": self.crime_count,
            "publish": self.published,
        }
