from sqlalchemy import Boolean, Column, Date, Integer, String, select

from app.constants import PageType, TransportType
from app.db import Base, get_session
from app.metro_logging import app_logger as logger


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
    sub_section_heading = Column(String)
    comments = Column(String)
    published = Column(Boolean)
    vetted = Column(Boolean)
    page_type = Column(String)

    def __repr__(self):
        return (
            f"AdminReview({self.year_month}, {self.year}, {self.month}, {self.fiscal_year},"
            f" {self.transport_type}, {self.line_name}, {self.section_heading}, {self.comments},"
            f" {self.published}, {self.page_type}, {self.vetted}, {self.sub_section_heading}"
        )

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
            "sub_section_heading": self.sub_section_heading,
            "comments": self.comments,
            "vetted": self.vetted,
            "page_type": self.page_type,
            "publish": self.published,
        }

    @staticmethod
    async def get_comment_by_id(admin_id: int) -> str:
        """
        Retrieves the comment associated with the given admin ID.

        Args:
            admin_id (int): The ID of the admin.

        Returns:
            str: The comment associated with the admin ID.
        """
        comment = ""
        ar = None
        async with get_session() as sess:
            ar: AdminReview = (
                await sess.scalars(select(AdminReview).where(AdminReview.id == admin_id))
            ).first()

        if ar:
            comment = ar.comments

        return comment

    @staticmethod
    async def get_comment(
        year_month,
        stat_type: str,
        line_name: str,
        transport_type: str,
        section_heading: str,
        published: bool,
        vetted: bool = None,
        sub_section_heading: str = None,
    ):
        comments = ""
        filters = [
            AdminReview.section_heading == section_heading,
            AdminReview.year_month == year_month,
            AdminReview.published == published,
        ]
        if vetted is not None:
            filters.append(AdminReview.vetted == vetted)

        page_type = getattr(PageType, stat_type.upper())

        if page_type:
            filters.append(AdminReview.page_type == page_type)
        else:
            logger.debug("Page type not found")

        if line_name:
            filters.append(AdminReview.line_name == line_name)
        else:
            filters.append(AdminReview.line_name == "all")

        if transport_type:
            filters.append(AdminReview.transport_type == transport_type)
        else:
            filters.append(AdminReview.transport_type == TransportType.SYSTEM_WIDE)

        if sub_section_heading is not None:
            if sub_section_heading:
                filters.append(AdminReview.sub_section_heading == sub_section_heading)
            else:
                filters.append(AdminReview.sub_section_heading == "all")

        async with get_session() as sess:
            comments = (await sess.scalars(select(AdminReview.comments).where(*filters))).first()

        return comments
