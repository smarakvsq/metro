from sqlalchemy import func, select

from app.constants import PageType
from app.db import get_session
from app.models.admin_review import AdminReview
from app.models.arrest import Arrest
from app.util import format_line_data


async def get_arrest_pie(json_data):
    line_name = json_data.get("line_name")
    transport_type = json_data.get("transport_type")
    gender = json_data.get("gender")
    dates = json_data.get("dates")
    published = json_data.get("published")

    filters = [Arrest.published == published, Arrest.gender == gender]

    if line_name:
        filters.append(Arrest.line_name == line_name)

    if transport_type:
        filters.append(Arrest.transport_type == transport_type)

    if dates:
        filters.append(Arrest.year_month.in_(dates))

    data = []
    formatted_data = []

    async with get_session() as sess:
        query = (
            select(
                Arrest.ethinicity,
                func.sum(Arrest.arrest_count).label("total_arrest_count"),
            )
            .where(*filters)
            .group_by(Arrest.ethinicity)
        )
        data = (await sess.execute(query)).all()
        formatted_data = {ethinicity: count for ethinicity, count in data if count != 0}

    arrest_data = {}
    if formatted_data:
        arrest_data.update({"arrest_pie_data": formatted_data})
    return arrest_data


async def get_arrest_line(json_data):
    line_name = json_data.get("line_name")
    transport_type = json_data.get("transport_type")
    gender = json_data.get("gender")
    dates = json_data.get("dates")
    published = json_data.get("published")

    filters = [Arrest.published == published, Arrest.gender == gender]

    if line_name:
        filters.append(Arrest.line_name == line_name)

    if transport_type:
        filters.append(Arrest.transport_type == transport_type)

    if dates:
        filters.append(Arrest.year_month.in_(dates))

    data = []

    async with get_session() as sess:
        query = (
            select(
                Arrest.year_month,
                Arrest.ethinicity,
                func.sum(Arrest.arrest_count).label("total_arrest_count"),
            )
            .where(*filters)
            .group_by(Arrest.year_month, Arrest.ethinicity)
            .order_by(Arrest.year_month)
        )
        data = (await sess.execute(query)).all()

    line_data = []

    if data:
        line_data = await format_line_data(data=data)

    arrest_data = {}
    if line_data:
        arrest_data.update({"arrest_line_data": line_data})
    return arrest_data


async def get_arrest_agency_wide_bar(json_data):
    line_name = json_data.get("line_name")
    transport_type = json_data.get("transport_type")
    gender = json_data.get("gender")
    dates = json_data.get("dates")
    published = json_data.get("published")

    filters = [Arrest.published == published, Arrest.gender == gender]

    if line_name:
        filters.append(Arrest.line_name == line_name)

    if transport_type:
        filters.append(Arrest.transport_type == transport_type)

    if dates:
        filters.append(Arrest.year_month.in_(dates))

    data = []
    formatted_data = []

    async with get_session() as sess:
        query = (
            select(
                Arrest.agency_name,
                func.sum(Arrest.arrest_count).label("total_arrest_count"),
            )
            .where(*filters)
            .group_by(Arrest.agency_name)
        )
        data = (await sess.execute(query)).all()
        formatted_data = {agency_name: count for agency_name, count in data if count != 0}

    arrest_data = {}
    if formatted_data:
        arrest_data.update({"arrest_agency_wide_bar": formatted_data})
    return arrest_data


async def get_arrest_agency_wide_line(json_data):
    line_name = json_data.get("line_name")
    transport_type = json_data.get("transport_type")
    gender = json_data.get("gender")
    dates = json_data.get("dates")
    published = json_data.get("published")

    filters = [Arrest.published == published, Arrest.gender == gender]

    if line_name:
        filters.append(Arrest.line_name == line_name)

    if transport_type:
        filters.append(Arrest.transport_type == transport_type)

    if dates:
        filters.append(Arrest.year_month.in_(dates))

    data = []

    async with get_session() as sess:
        query = (
            select(
                Arrest.year_month,
                Arrest.agency_name,
                func.sum(Arrest.arrest_count).label("total_arrest_count"),
            )
            .where(*filters)
            .group_by(Arrest.year_month, Arrest.agency_name)
            .order_by(Arrest.year_month)
        )
        data = (await sess.execute(query)).all()

    line_data = []

    if data:
        line_data = await format_line_data(data=data)

    arrest_data = {}
    if line_data:
        arrest_data.update({"arrest_agency_wide_line": line_data})
    return arrest_data


async def get_arrest_comment(
    line_name: str, transport_type: str, section_heading: str, year_month, published: bool
):
    comment = ""

    try:
        comment = await AdminReview.get_comment(
            year_month=year_month,
            stat_type=PageType.ARREST,
            line_name=line_name,
            transport_type=transport_type,
            section_heading=section_heading,
            published=published,
        )
    except Exception as exc:
        print(exc)

    return comment or ""


async def get_year_months(published: bool, transport_type: str):
    data = []
    filters = [Arrest.published == published]

    if transport_type:
        filters.append(Arrest.transport_type == transport_type)

    async with get_session() as sess:
        query = (
            select(Arrest.year_month).where(*filters).distinct().order_by(Arrest.year_month.desc())
        )
        data = (await sess.scalars(query)).all()
    return data
