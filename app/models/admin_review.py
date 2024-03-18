import asyncio
from typing import Optional
from datetime import date
from sqlalchemy import Column, Integer, Date, String, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Base

class AdminReview(Base):
    __tablename__ = "admin_review"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year_month = Column(Date)
    year = Column(Integer)
    month = Column(Integer)
    fiscal_year = Column(String)
    transport_type = Column(String)
    line_type = Column(String)
    section_heading = Column(String)
    comments = Column(String)
    publish = Column(Boolean)
    vetted = Column(Boolean)

    def __repr__(self):
        return f"AdminReview({self.year_month}, {self.year}, {self.month}, {self.fiscal_year}, {self.transport_type}, {self.line_type}, {self.section_heading}, {self.comments}, {self.publish}, {self.vetted})"

    def __str__(self):
        return self.__repr__()

    def to_json(self):
        return {
            "year_month": str(self.year_month),
            "year": self.year,
            "month": self.month,
            "fiscal_year": self.fiscal_year,
            "transport_type": self.transport_type,
            "line_type": self.line_type,
            "section_heading": self.section_heading,
            "comments": self.comments,
            "publish": self.preview_publish,
            "vetted": self.vetted_unvetted,
        }

async def create_admin_review(
    session: AsyncSession,
    year_month: date,
    year: int,
    month: int,
    fiscal_year: str,
    transport_type: str,
    line_type: str,
    section_heading: str,
    comments: str,
    preview_publish: str,
    vetted_unvetted: str,
) -> AdminReview:
    admin_review = AdminReview(
        year_month=year_month,
        year=year,
        month=month,
        fiscal_year=fiscal_year,
        transport_type=transport_type,
        linetype=line_type,
        section_heading=section_heading,
        comments=comments,
        preview_publish=preview_publish,
        vetted_unvetted=vetted_unvetted,
    )
    session.add(admin_review)
    await session.commit()
    return admin_review

# ... (read_admin_review, update_admin_review, and delete_admin_review methods remain the same) ...

# async def main():
#     engine = create_async_engine("sqlite+aiosqlite:///admin_review.db", echo=True)
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

#     async with AsyncSession(engine) as session:
#         new_admin_review = await create_admin_review(
#             session,
#             year_month=date(2023, 3, 1),
#             year=2023,
#             month=3,
#             fiscal_year="2023-2024",
#             transport_type="Air",
#             linetype="Domestic",
#             section_heading="Revenue",
#             comments="No comments",
#             preview_publish="Publish",
#             vetted_unvetted="Vetted",
#         )
#         print(new_admin_review)
#         print(new_admin_review.to_json())

# asyncio.run(main())

print(Base.metadata.tables)