from sqlalchemy import func, select
from werkzeug.exceptions import NotImplemented

from app.constants import CrimeSeverity, PageType, Ucr
from app.db import get_session
from app.metro_logging import app_logger as logger
from app.models.admin_review import AdminReview
from app.models.crime_unvet import CrimeUnvetted


async def get_unvetted_date(published, transport_type):
    data = []

    filters = [CrimeUnvetted.published == published]

    if transport_type:
        filters.append(CrimeUnvetted.transport_type == transport_type)

    async with get_session() as sess:
        query = (
            select(CrimeUnvetted.year_month, CrimeUnvetted.week_no)
            .where(*filters)
            .group_by(CrimeUnvetted.year_month, CrimeUnvetted.week_no)
            .order_by(CrimeUnvetted.year_month.desc())
        )
        data = (await sess.execute(query)).all()
    date_dict = {}
    if data:
        for date_, week in data:
            date_ = date_.strftime("%Y-%-m-%-d")
            if date_ not in date_dict.keys():
                date_dict[date_] = [week]
            else:
                date_dict[date_].append(week)

        date_dict = [{date_: sorted(week_list)} for date_, week_list in date_dict.items()]

    return date_dict


async def get_crime_unvetted_data_bar(json_data: dict):
    line_name = json_data.get("line_name")
    transport_type = json_data.get("transport_type")
    severity = json_data.get("severity")
    year_months = json_data.get("year_months")
    weeks = json_data.get("weeks")
    ucr = json_data.get("crime_category")
    published = json_data.get("published")

    filters = [
        CrimeUnvetted.published == published,
    ]

    if severity and severity == CrimeSeverity.VIOLENT_CRIME:
        filters.append(CrimeUnvetted.ucr == Ucr.PERSONS)

    if ucr:
        filters.append(CrimeUnvetted.ucr == ucr)

    if line_name:
        filters.append(CrimeUnvetted.line_name == line_name)

    if transport_type:
        filters.append(CrimeUnvetted.transport_type == transport_type)

    if year_months:
        filters.append(CrimeUnvetted.year_month.in_(year_months))

    if weeks:
        filters.append(CrimeUnvetted.week_no.in_(weeks))

    json_data = []
    async with get_session() as sess:
        query = (
            select(
                CrimeUnvetted.crime_name,
                func.sum(CrimeUnvetted.crime_count).label("total_crime_count"),
            )
            .where(*filters)
            .where(CrimeUnvetted.crime_name != None)
            .group_by(CrimeUnvetted.crime_name)
        )
        data = (await sess.execute(query)).all()
    if data:
        json_data = {crime_name: count for crime_name, count in data if count != 0}
        json_data = dict(sorted(json_data.items(), key=lambda x: x[1], reverse=True))

    crime_data = {}
    crime_data.update({"crime_unvetted_bar_data": json_data})
    return crime_data


async def get_crime_unvetted_data_line(json_data):
    line_name = json_data.get("line_name")
    transport_type = json_data.get("transport_type")
    severity = json_data.get("severity")
    year_months = json_data.get("year_months")
    weeks = json_data.get("weeks")
    ucr = json_data.get("crime_category")
    published = json_data.get("published")

    filters = [
        CrimeUnvetted.published == published,
    ]

    if severity and severity == CrimeSeverity.VIOLENT_CRIME:
        filters.append(CrimeUnvetted.ucr == Ucr.PERSONS)

    if ucr:
        filters.append(CrimeUnvetted.ucr == ucr)

    if line_name:
        filters.append(CrimeUnvetted.line_name == line_name)

    if transport_type:
        filters.append(CrimeUnvetted.transport_type == transport_type)

    if year_months:
        filters.append(CrimeUnvetted.year_month.in_(year_months))

    if weeks:
        filters.append(CrimeUnvetted.week_no.in_(weeks))

    line_data = []

    data = []
    async with get_session() as sess:
        query = (
            select(
                CrimeUnvetted.year_month,
                CrimeUnvetted.week_no,
                CrimeUnvetted.crime_name,
                func.sum(CrimeUnvetted.crime_count).label("total_crime_count"),
            )
            .where(*filters)
            .where(
                CrimeUnvetted.crime_name != None,
                CrimeUnvetted.year_month != None,
                CrimeUnvetted.week_no != None,
            )
            .group_by(CrimeUnvetted.year_month, CrimeUnvetted.week_no, CrimeUnvetted.crime_name)
            .order_by(CrimeUnvetted.year_month, CrimeUnvetted.week_no)
        )
        data = (await sess.execute(query)).all()

    if data:
        crime_types = set(item[2] for item in data)
        for item in data:
            date, week, _, value = item
            crime_dict = {"name": str(date), "week": week}
            for crime_type in crime_types:
                crime_dict[crime_type] = 0
            crime_dict[item[2]] = value
            line_data.append(crime_dict)

    return line_data


async def get_crime_unvetted_data_agency_bar(json_data):
    line_name = json_data.get("line_name")
    transport_type = json_data.get("transport_type")
    severity = json_data.get("severity")
    year_months = json_data.get("year_months")
    weeks = json_data.get("weeks")
    ucr = json_data.get("crime_category")
    published = json_data.get("published")

    filters = [
        CrimeUnvetted.published == published,
    ]

    if severity and severity == CrimeSeverity.VIOLENT_CRIME:
        filters.append(CrimeUnvetted.ucr == Ucr.PERSONS)

    if ucr:
        filters.append(CrimeUnvetted.ucr == ucr)

    if line_name:
        filters.append(CrimeUnvetted.line_name == line_name)

    if transport_type:
        filters.append(CrimeUnvetted.transport_type == transport_type)

    if year_months:
        filters.append(CrimeUnvetted.year_month.in_(year_months))

    if weeks:
        filters.append(CrimeUnvetted.week_no.in_(weeks))

    json_data = []

    async with get_session() as sess:
        query = (
            select(
                CrimeUnvetted.agency_name,
                func.sum(CrimeUnvetted.crime_count).label("total_crime_count"),
            )
            .where(*filters)
            .where(CrimeUnvetted.agency_name != None)
            .group_by(CrimeUnvetted.agency_name)
            .order_by("total_crime_count")
        )
        data = (await sess.execute(query)).all()

    if data:
        json_data = {agency_name: count for agency_name, count in data if count != 0}
        json_data = dict(sorted(json_data.items(), key=lambda x: x[1], reverse=True))

    crime_data = {}
    crime_data.update({"unvetted_agency_wide_bar_data": json_data})

    return crime_data


async def get_crime_unvetted_data_agency_line(json_data):
    line_name = json_data.get("line_name")
    transport_type = json_data.get("transport_type")
    severity = json_data.get("severity")
    year_months = json_data.get("year_months")
    weeks = json_data.get("weeks")
    ucr = json_data.get("crime_category")
    published = json_data.get("published")

    filters = [
        CrimeUnvetted.published == published,
    ]

    if severity and severity == CrimeSeverity.VIOLENT_CRIME:
        filters.append(CrimeUnvetted.ucr == Ucr.PERSONS)

    if ucr:
        filters.append(CrimeUnvetted.ucr == ucr)

    if line_name:
        filters.append(CrimeUnvetted.line_name == line_name)

    if transport_type:
        filters.append(CrimeUnvetted.transport_type == transport_type)

    if year_months:
        filters.append(CrimeUnvetted.year_month.in_(year_months))

    if weeks:
        filters.append(CrimeUnvetted.week_no.in_(weeks))

    json_data = []

    async with get_session() as sess:
        query = (
            select(
                CrimeUnvetted.year_month,
                CrimeUnvetted.week_no,
                CrimeUnvetted.agency_name,
                func.sum(CrimeUnvetted.crime_count).label("total_crime_count"),
            )
            .where(*filters)
            .where(
                CrimeUnvetted.agency_name != None,
                CrimeUnvetted.year_month != None,
                CrimeUnvetted.week_no != None,
                CrimeUnvetted.crime_count != None,
            )
            .group_by(CrimeUnvetted.year_month, CrimeUnvetted.week_no, CrimeUnvetted.agency_name)
            .order_by(CrimeUnvetted.year_month, CrimeUnvetted.week_no)
        )
        data = (await sess.execute(query)).all()

    return json_data


async def get_unvetted_crime_comment(
    vetted: bool,
    line_name: str,
    transport_type: str,
    section_heading: str,
    sub_section_heading: str,
    year_month,
    published: bool,
):
    raise NotImplemented("Call /crime/comment with vetted=False")
