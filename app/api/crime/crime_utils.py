from datetime import date

from sqlalchemy import and_, func, select

from app.constants import CrimeSectionHeading, PageType, TransportType
from app.db import get_session
from app.models.admin_review import AdminReview
from app.util import select_crime_table

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
            .group_by(Table.crime_name)
        )
        data = (await sess.execute(query)).all()
        json_data = {crime_name: count for crime_name, count in data}

    crime_data = {}
    if json_data:
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
    formatted_data = []
    async with get_session() as sess:
        query = (
            select(
                Table.year_month,
                Table.crime_name,
                func.sum(Table.crime_count).label("total_crime_count"),
            )
            .where(*filters)
            .group_by(Table.year_month, Table.crime_name)
        )
        data = (await sess.execute(query)).all()
        if data:
            formatted_data = {}
            for month, crime, count in data:
                month = month.strftime("%b-%Y")
                if month not in formatted_data:
                    formatted_data[month] = {}
                formatted_data[month][crime] = count

    crime_data = {}
    if formatted_data:
        crime_data.update({"crime_line_data": formatted_data})

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
            .group_by(Table.agency_name)
        )
        data = (await sess.execute(query)).all()
        json_data = {agency_name: count for agency_name, count in data}

    crime_data = {}
    if json_data:
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
    async with get_session() as sess:
        query = (
            select(
                Table.year_month,
                Table.agency_name,
                func.sum(Table.crime_count).label("total_crime_count"),
            )
            .where(*filters)
            .group_by(Table.year_month, Table.agency_name)
        )
        data = (await sess.execute(query)).all()

    if data:
        formatted_data = {}
        for month, crime, count in data:
            month = month.strftime("%b-%Y")
            if month not in formatted_data:
                formatted_data[month] = {}
            formatted_data[month][crime] = count

    crime_data = {}
    if formatted_data:
        crime_data.update({"agency_wide_line_data": formatted_data})

    return crime_data


async def get_crime_comment(
    vetted: bool,
    line_name: str,
    transport_type: str,
    section_heading: str,
    sub_section_heading: str,
    year_month,
    published: bool
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
            published=published
        )
    except Exception as exc:
        print(exc)

    return comment or ""


async def get_year_months_for_comment(json_data: dict):
    line_name = json_data.get("line_name")
    transport_type = json_data.get("transport_type")
    from_date = json_data.get("from_date")
    to_date = json_data.get("to_date")
    severity = json_data.get("section")
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

    if from_date and to_date:
        filters.append(
            and_(
                Table.year_month >= from_date,
                Table.year_month < to_date,
            )
        )

    data = []
    async with get_session() as sess:
        query = select(Table.year_month).where(*filters).distinct()
        data = (await sess.scalars(query)).all()
    return data


async def get_year_months(vetted: bool, published: bool, transport_type: str):
    data = []
    
    Table = await select_crime_table(vetted=vetted)
    filters = [Table.published == published]

    if transport_type:
        filters.append(Table.transport_type == transport_type)

    async with get_session() as sess:
        query = select(Table.year_month).where(*filters).distinct().order_by(Table.year_month.desc())
        data = (await sess.scalars(query)).all()
    return data