from sqlalchemy import Column, Integer, Date, String, Boolean
from app.db import Base


class CallsForServiceLanding(Base):
    __tablename__ = "calls_for_service_landing"
    __table_args__ = {"schema": "ssle_metro"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    transport_type = Column(String)
    current_year_month = Column(Date)
    current_month_count = Column(Integer)
    current_year_count = Column(Integer)
    previous_year_month_count = Column(Integer)
    previous_year_month_count_percent = Column(Integer)
    previous_month_count = Column(Integer)
    previous_month_count_percent = Column(Integer)
    admin_review_id = Column(Integer)
    published = Column(Boolean)

    def __repr__(self):
        return f"CallsForServiceLanding({self.transport_type}, {self.current_year_month}, {self.current_month_count}, {self.current_year_count}, {self.previous_year_month_count}, {self.previous_year_month_count_percent}, {self.previous_month_count}, {self.previous_month_count_percent}, {self.admin_review_id}, {self.published})"

    def __str__(self):
        return self.__repr__()

    def to_json(self):
        return {
            "transport_type": self.transport_type,
            "current_year_month": str(self.current_year_month),
            "current_month_count": self.current_month_count,
            "current_year_count": self.current_year_count,
            "previous_year_month_count": self.previous_year_month_count,
            "previous_year_month_count_percent": self.previous_year_month_count_percent,
            "previous_month_count": self.previous_month_count,
            "previous_month_count_percent": self.previous_month_count_percent,
            "admin_review_id": self.admin_review_id,
            "published": self.published,
        }


class ArrestLanding(Base):
    __tablename__ = "arrest_landing"
    __table_args__ = {"schema": "ssle_metro"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    transport_type = Column(String)
    current_year_month = Column(Date)
    current_month_count = Column(Integer)
    current_year_count = Column(Integer)
    previous_year_count = Column(Integer)
    previous_year_count_percent = Column(Integer)
    previous_month_count = Column(Integer)
    previous_month_count_percent = Column(Integer)
    admin_review_id = Column(Integer)
    published = Column(Boolean)

    def __repr__(self):
        return f"ArrestLanding({self.transport_type}, {self.current_year_month}, {self.current_month_count}, {self.current_year_count}, {self.previous_year_count}, {self.previous_year_count_percent}, {self.previous_month_count}, {self.previous_month_count_percent}, {self.admin_review_id}, {self.published})"

    def __str__(self):
        return self.__repr__()

    def to_json(self):
        return {
            "transport_type": self.transport_type,
            "current_year_month": str(self.current_year_month),
            "current_month_count": self.current_month_count,
            "current_year_count": self.current_year_count,
            "previous_year_count": self.previous_year_count,
            "previous_year_count_percent": self.previous_year_count_percent,
            "previous_month_count": self.previous_month_count,
            "previous_month_count_percent": self.previous_month_count_percent,
            "admin_review_id": self.admin_review_id,
            "published": self.published,
        }


class CrimeLanding(Base):
    __tablename__ = "crime_landing"
    __table_args__ = {"schema": "ssle_metro"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    transport_type = Column(String)
    current_year_month = Column(Date)
    current_month_count = Column(Integer)
    current_year_count = Column(Integer)
    total_boardings = Column(Integer)
    crime_per_100k_boardings = Column(Integer)
    previous_year_count = Column(Integer)
    previous_year_count_percent = Column(Integer)
    previous_month_count = Column(Integer)
    previous_month_count_percent = Column(Integer)
    admin_review_id = Column(Integer)
    published = Column(Boolean)

    def __repr__(self):
        return f"CrimeLanding({self.transport_type}, {self.current_year_month}, {self.current_month_count}, {self.current_year_count}, {self.total_boardings}, {self.crime_per_100k_boardings}, {self.previous_year_count}, {self.previous_year_count_percent}, {self.previous_month_count}, {self.previous_month_count_percent}, {self.admin_review_id}, {self.published})"

    def __str__(self):
        return self.__repr__()

    def to_json(self):
        return {
            "transport_type": self.transport_type,
            "current_year_month": str(self.current_year_month),
            "current_month_count": self.current_month_count,
            "current_year_count": self.current_year_count,
            "total_boardings": self.total_boardings,
            "crime_per_100k_boardings": self.crime_per_100k_boardings,
            "previous_year_count": self.previous_year_count,
            "previous_year_count_percent": self.previous_year_count_percent,
            "previous_month_count": self.previous_month_count,
            "previous_month_count_percent": self.previous_month_count_percent,
            "admin_review_id": self.admin_review_id,
            "published": self.published,
        }
