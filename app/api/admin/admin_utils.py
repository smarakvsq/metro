from app.db import get_session
from app.models import AdminReview
from app.constants import TransportType
from app.util import parse_date

from sqlalchemy import func, select, update


async def update_comments(page_type: str, line_name: str, transport_type: str, year_month: str, comment_info: list):
    year_month = await parse_date(year_month)

    filters = [AdminReview.page_type == page_type, AdminReview.year_month == year_month]

    if line_name:
        filters.append(AdminReview.line_name == line_name)
    else:
        filters.append(AdminReview.line_name == "all")
    
    if transport_type:
        filters.append(AdminReview.transport_type == transport_type)
    else:
        filters.append(AdminReview.transport_type == TransportType.SYSTEM_WIDE)

    for info in comment_info:
        section_filters = []
        section = info.get("section")
        sub_section = info.get("sub_section")
        comment = info.get("comment")

        if section:
            section_filters.append(AdminReview.section_heading == section)
        
        if sub_section:
            section_filters.append(AdminReview.sub_section_heading == sub_section)

        async with get_session() as sess:
            query = (
                update(AdminReview).where(*filters).where(section_filters).values({"comments": comment})
            )
            await sess.execute(query)
        