from sqlalchemy import select, and_, or_

from app.constants import PageType, TransportType, CrimeSectionHeading
from app.db import get_session
from app.util import select_crime_table
from app.models.admin_review import AdminReview


async def get_unique_ucr(route: str, vetted: bool, transport_type: str, severity: str):
    data = []
    filters = [Table.transport_type == transport_type, Table.severity == severity]
    Table = await select_crime_table(vetted)
    if route:
        filters.append(Table.route_name == route)
    async with get_session() as sess:
        data = (await sess.scalars(select(Table.ucr).where(*filters).distinct())).all()

    return data


async def get_crime_data(json_data):
    route_name = json_data.get("route_name")
    transport_type = json_data.get("transport_type")
    from_date = json_data.get("from_date")
    to_date = json_data.get("to_date")
    severity = json_data.get("severity")
    ucr = json_data.get("crime_category")
    vetted = json_data.get("vetted")
    published = json_data.get("published")

    crime_comment = ""
    severity_mapper = {
        CrimeSectionHeading.SERIOUS_CRIME: "PART 2",
        CrimeSectionHeading.GENERAL_CRIME: "PART 1",
    }

    Table = await select_crime_table(vetted)

    filters = [
        Table.ucr == ucr,
        Table.published == published,
    ]

    if severity in severity_mapper.keys():
        filters.append(Table.severity == severity_mapper[severity])

    if route_name:
        filters.append(Table.line_name == route_name)

    if transport_type:
        filters.append(Table.transport_type == transport_type)

    if from_date and to_date:
        # from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
        # to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")
        filters.append(
            and_(
                Table.year_month >= from_date,
                Table.year_month <= to_date,
            )
        )

    data = []
    json_data = []
    async with get_session() as sess:
        data = (
            await sess.scalars(select(Table).where(*filters).order_by(Table.year_month.desc()))
        ).all()
        json_data = [dict(instance._asdict()) for instance in data]
    
    crime_data = {}
    if json_data:
        crime_data.update({"crime_data": json_data})
        unique_year_months = set([x.year_month for x in data])
        if len(unique_year_months) == 1:
            crime_comment = await get_crime_comment(
                vetted=vetted,
                line_name=route_name,
                transport_type=transport_type,
                section_heading=severity,
                year_month=unique_year_months[0],
                sub_section_heading=ucr,
            )
            crime_data.update({"comment": crime_comment})
        
    return crime_data


async def get_crime_data_agency(json_data):
    route_name = json_data.get("route_name")
    transport_type = json_data.get("transport_type")
    from_date = json_data.get("from_date")
    to_date = json_data.get("to_date")
    severity = json_data.get("severity")
    ucr = json_data.get("crime_category")
    vetted = json_data.get("vetted")
    published = json_data.get("published")

    crime_comment = ""
    severity_mapper = {
        CrimeSectionHeading.SERIOUS_CRIME: "PART 2",
        CrimeSectionHeading.GENERAL_CRIME: "PART 1",
    }

    Table = await select_crime_table(vetted)

    filters = [
        Table.ucr == ucr,
        Table.published == published,
    ]

    if severity in severity_mapper.keys():
        filters.append(Table.severity == severity_mapper[severity])

    if route_name:
        filters.append(Table.line_name == route_name)

    if transport_type:
        filters.append(Table.transport_type == transport_type)

    if from_date and to_date:
        # from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
        # to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")
        filters.append(
            and_(
                Table.year_month >= from_date,
                Table.year_month <= to_date,
            )
        )

    data = []
    json_data = []
    async with get_session() as sess:
        data = (
            await sess.scalars(select(Table).where(*filters).order_by(Table.year_month.desc()))
        ).all()
        json_data = [dict(instance._asdict()) for instance in data]
    
    crime_data = {}
    if json_data:
        crime_data.update({"crime_data": json_data})
        unique_year_months = set([x.year_month for x in data])
        if len(unique_year_months) == 1:
            crime_comment = await get_crime_comment(
                vetted=vetted,
                line_name=route_name,
                transport_type=transport_type,
                section_heading=severity,
                year_month=unique_year_months[0],
                sub_section_heading=ucr,
            )
            crime_data.update({"comment": crime_comment})
        
    return crime_data

async def get_crime_comment(
    vetted: bool,
    line_name: str,
    transport_type: str,
    section_heading: str,
    sub_section_heading: str,
    year_month,
):
    comment = ""
    try:
        comment = AdminReview.get_comment(
            year_month=year_month,
            stat_type=PageType.CRIME,
            vetted=vetted,
            line_name=line_name,
            transport_type=transport_type,
            section_heading=section_heading,
            sub_section_heading=sub_section_heading,
        )
    except Exception as exc:
        print(exc)

    return comment
