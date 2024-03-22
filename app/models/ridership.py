from sqlalchemy import Column, Integer, String, Float
from app.db import Base


class RidersSummary(Base):
    __tablename__ = "riders_summary"
    __table_args__ = {"schema": "ssle_metro"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer)
    month_number = Column(Integer)
    day_type = Column(String)
    line_name = Column(String)
    provider = Column(String)
    date_count = Column(Integer)
    avg_daily_riders = Column(Float)
    avg_daily_pmiles = Column(Float)
    riders_total = Column(Integer)
    pmiles_total = Column(Integer)

    def __repr__(self):
        return f"RidersSummary({self.year}, {self.month_number}, {self.day_type}, {self.line_name}, {self.provider}, {self.date_count}, {self.avg_daily_riders}, {self.avg_daily_pmiles}, {self.riders_total}, {self.pmiles_total})"

    def __str__(self):
        return self.__repr__()

    def to_json(self):
        return {
            "year": self.year,
            "month_number": self.month_number,
            "day_type": self.day_type,
            "line_name": self.line_name,
            "provider": self.provider,
            "date_count": self.date_count,
            "avg_daily_riders": self.avg_daily_riders,
            "avg_daily_pmiles": self.avg_daily_pmiles,
            "riders_total": self.riders_total,
            "pmiles_total": self.pmiles_total,
        }
