from sqlalchemy import and_, func, select

from app.constants import CrimeSectionHeading, PageType
from app.db import get_session
from app.models.admin_review import AdminReview
from app.util import format_line_data, select_crime_table

severity_mapper = {
    CrimeSectionHeading.SERIOUS_CRIME: "part_2",
    CrimeSectionHeading.GENERAL_CRIME: "part_1",
}


async def get_unique_ucr(line_name: str, vetted: bool, transport_type: str, severity: str):
    data = []
    Table = await select_crime_table(vetted)
    filters = [Table.transport_type == transport_type]

    if severity in severity_mapper.keys():
        filters.append(Table.severity == severity_mapper[severity])

    if line_name:
        filters.append(Table.line_name == line_name)

    async with get_session() as sess:
        data = (await sess.scalars(select(Table.ucr).where(*filters).distinct())).all()

    return data


async def get_crime_data_bar(json_data):
    line_name = json_data.get("line_name")
    transport_type = json_data.get("transport_type")
    severity = json_data.get("severity")
    dates = json_data.get("dates")
    ucr = json_data.get("crime_category")
    vetted = json_data.get("vetted")
    published = json_data.get("published")

    Table = await select_crime_table(vetted)

    filters = [
        Table.published == published,
    ]

    if severity in severity_mapper.keys():
        filters.append(Table.severity == severity_mapper[severity])

    if ucr:
        filters.append(Table.ucr == ucr)

    if line_name:
        filters.append(Table.line_name == line_name)

    if transport_type:
        filters.append(Table.transport_type == transport_type)

    if dates:
        filters.append(Table.year_month.in_(dates))

    data = []
    json_data = []
    async with get_session() as sess:
        query = (
            select(Table.crime_name, func.sum(Table.crime_count).label("total_crime_count"))
            .where(*filters)
            .where(Table.crime_name != None)
            .group_by(Table.crime_name)
        )
        data = (await sess.execute(query)).all()
        json_data = {crime_name: count for crime_name, count in data if count != 0}

    crime_data = {}
    crime_data.update({"crime_bar_data": json_data})
    return crime_data


async def get_crime_data_line(json_data):
    line_name = json_data.get("line_name")
    transport_type = json_data.get("transport_type")
    dates = json_data.get("dates")
    severity = json_data.get("severity")
    ucr = json_data.get("crime_category")
    vetted = json_data.get("vetted")
    published = json_data.get("published")

    Table = await select_crime_table(vetted)

    filters = [
        Table.published == published,
    ]

    if severity in severity_mapper.keys():
        filters.append(Table.severity == severity_mapper[severity])

    if ucr:
        filters.append(Table.ucr == ucr)

    if line_name:
        filters.append(Table.line_name == line_name)

    if transport_type:
        filters.append(Table.transport_type == transport_type)

    if dates:
        filters.append(Table.year_month.in_(dates))

    data = []
    async with get_session() as sess:
        query = (
            select(
                Table.year_month,
                Table.crime_name,
                func.sum(Table.crime_count).label("total_crime_count"),
            )
            .where(*filters)
            .where(Table.crime_name != None)
            .group_by(Table.year_month, Table.crime_name)
            .order_by(Table.year_month)
        )
        data = (await sess.execute(query)).all()

    line_data = []
    if data:
        line_data = await format_line_data(data=data)

    crime_data = {}
    crime_data.update({"crime_line_data": line_data})

    return crime_data


async def get_crime_data_agency_bar(json_data):
    line_name = json_data.get("line_name")
    transport_type = json_data.get("transport_type")
    dates = json_data.get("dates")
    ucr = json_data.get("crime_category")
    vetted = json_data.get("vetted")
    published = json_data.get("published")

    Table = await select_crime_table(vetted)

    filters = [
        Table.published == published,
    ]

    if line_name:
        filters.append(Table.line_name == line_name)

    if ucr:
        filters.append(Table.ucr == ucr)

    if transport_type:
        filters.append(Table.transport_type == transport_type)

    if dates:
        filters.append(Table.year_month.in_(dates))

    data = []
    json_data = {}
    async with get_session() as sess:
        query = (
            select(Table.agency_name, func.sum(Table.crime_count).label("total_crime_count"))
            .where(*filters)
            .where(Table.agency_name != None)
            .group_by(Table.agency_name)
            .order_by("total_crime_count")
        )
        data = (await sess.execute(query)).all()
        json_data = {agency_name: count for agency_name, count in data if count != 0}

    crime_data = {}
    crime_data.update({"agency_wide_bar_data": json_data})

    return crime_data


async def get_crime_data_agency_line(json_data):
    line_name = json_data.get("line_name")
    transport_type = json_data.get("transport_type")
    dates = json_data.get("dates")
    ucr = json_data.get("crime_category")
    vetted = json_data.get("vetted")
    published = json_data.get("published")

    Table = await select_crime_table(vetted)

    filters = [
        Table.published == published,
    ]

    if ucr:
        filters.append(Table.ucr == ucr)

    if line_name:
        filters.append(Table.line_name == line_name)

    if transport_type:
        filters.append(Table.transport_type == transport_type)

    if dates:
        filters.append(Table.year_month.in_(dates))

    data = []
    line_data = []
    async with get_session() as sess:
        query = (
            select(
                Table.year_month,
                Table.agency_name,
                func.sum(Table.crime_count).label("total_crime_count"),
            )
            .where(*filters)
            .where(Table.agency_name != None)
            .group_by(Table.year_month, Table.agency_name)
            .order_by(Table.year_month)
        )
        data = (await sess.execute(query)).all()

    if data:
        line_data = await format_line_data(data=data)

    crime_data = {}
    crime_data.update({"agency_wide_line_data": line_data})

    return crime_data


async def get_crime_comment(
    vetted: bool,
    line_name: str,
    transport_type: str,
    section_heading: str,
    sub_section_heading: str,
    year_month,
    published: bool,
):
    comment = ""

    try:
        comment = await AdminReview.get_comment(
            year_month=year_month,
            stat_type=PageType.CRIME,
            vetted=vetted,
            line_name=line_name,
            transport_type=transport_type,
            section_heading=section_heading,
            sub_section_heading=sub_section_heading,
            published=published,
        )
    except Exception as exc:
        print(exc)

    return comment or ""

async def get_year_months(vetted: bool, published: bool, transport_type: str):
    data = []

    Table = await select_crime_table(vetted=vetted)
    filters = [Table.published == published]

    if transport_type:
        filters.append(Table.transport_type == transport_type)

    async with get_session() as sess:
        query = (
            select(Table.year_month).where(*filters).distinct().order_by(Table.year_month.desc())
        )
        data = (await sess.scalars(query)).all()
    return data
