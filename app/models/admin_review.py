from sqlalchemy import Column, Integer, Date, String, Boolean, select
from app.db import Base, get_session


class AdminReview(Base):
    __tablename__ = "admin_review"
    __table_args__ = {"schema": "ssle_metro"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    year_month = Column(Date)
    year = Column(Integer)
    month = Column(String)
    fiscal_year = Column(String)
    transport_type = Column(String)
    line_name = Column(String)
    section_heading = Column(String)
    comments = Column(String)
    published = Column(Boolean)

    def __repr__(self):
        return f"AdminReview({self.year_month}, {self.year}, {self.month}, {self.fiscal_year}, {self.transport_type}, {self.line_name}, {self.section_heading}, {self.comments}, {self.published}"

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
            "section_heading": self.section_heading,
            "comments": self.comments,
            "publish": self.published,
        }

    @staticmethod
    async def get_comment(admin_id: int) -> str:
        comment = ""
        async with get_session() as sess:
            ar: AdminReview = (await sess.scalars(select(AdminReview).where(AdminReview.id == admin_id))).first()

        if ar:
            comment = ar.comments

        return comment
