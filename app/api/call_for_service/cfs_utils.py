from sqlalchemy import and_, func, select

from app.constants import PageType
from app.db import get_session
from app.models.admin_review import AdminReview
from app.models.call_for_service import CallForService
from app.util import format_line_data


async def get_call_for_service_bar(json_data):
    line_name = json_data.get("line_name")
    transport_type = json_data.get("transport_type")
    dates = json_data.get("dates")
    published = json_data.get("published")

    filters = [
        CallForService.published == published,
    ]

    if line_name:
        filters.append(CallForService.line_name == line_name)

    if transport_type:
        filters.append(CallForService.transport_type == transport_type)

    if dates:
        filters.append(CallForService.year_month.in_(dates))

    data = []
    formatted_data = []

    async with get_session() as sess:
        query = (
            select(
                CallForService.call_type,
                func.sum(CallForService.calls_count).label("total_call_count"),
            )
            .where(*filters)
            .group_by(CallForService.call_type)
        )
        data = (await sess.execute(query)).all()
        formatted_data = {call_type: count for call_type, count in data if count != 0}

    call_for_service_data = {}
    if formatted_data:
        call_for_service_data.update({"call_for_service_bar_data": formatted_data})
    return call_for_service_data


async def get_call_for_service_line(json_data):
    line_name = json_data.get("line_name")
    transport_type = json_data.get("transport_type")
    dates = json_data.get("dates")
    published = json_data.get("published")

    filters = [
        CallForService.published == published,
    ]

    if line_name:
        filters.append(CallForService.line_name == line_name)

    if transport_type:
        filters.append(CallForService.transport_type == transport_type)

    if dates:
        filters.append(CallForService.year_month.in_(dates))

    data = []

    async with get_session() as sess:
        query = (
            select(
                CallForService.year_month,
                CallForService.call_type,
                func.sum(CallForService.calls_count).label("total_call_count"),
            )
            .where(*filters)
            .group_by(CallForService.year_month, CallForService.call_type)
            .order_by(CallForService.year_month)
        )
        data = (await sess.execute(query)).all()

    line_data = []

    if data:
        line_data = await format_line_data(data=data)

    call_for_service_data = {}
    if line_data:
        call_for_service_data.update({"call_for_service_line_data": line_data})
    return call_for_service_data


async def get_call_for_service_agency_wide_bar(json_data):
    line_name = json_data.get("line_name")
    transport_type = json_data.get("transport_type")
    dates = json_data.get("dates")
    published = json_data.get("published")

    filters = [
        CallForService.published == published,
    ]

    if line_name:
        filters.append(CallForService.line_name == line_name)

    if transport_type:
        filters.append(CallForService.transport_type == transport_type)

    if dates:
        filters.append(CallForService.year_month.in_(dates))

    data = []
    formatted_data = []

    async with get_session() as sess:
        query = (
            select(
                CallForService.agency_name,
                func.sum(CallForService.calls_count).label("total_call_count"),
            )
            .where(*filters)
            .group_by(CallForService.agency_name)
        )
        data = (await sess.execute(query)).all()
        formatted_data = {agency_name: count for agency_name, count in data if count != 0}

    call_for_service_data = {}
    if formatted_data:
        call_for_service_data.update({"call_for_service_agency_wide_bar": formatted_data})
    return call_for_service_data


async def get_call_for_service_agency_wide_line(json_data):
    line_name = json_data.get("line_name")
    transport_type = json_data.get("transport_type")
    dates = json_data.get("dates")
    published = json_data.get("published")

    filters = [
        CallForService.published == published,
    ]

    if line_name:
        filters.append(CallForService.line_name == line_name)

    if transport_type:
        filters.append(CallForService.transport_type == transport_type)

    if dates:
        filters.append(CallForService.year_month.in_(dates))

    data = []

    async with get_session() as sess:
        query = (
            select(
                CallForService.year_month,
                CallForService.agency_name,
                func.sum(CallForService.calls_count).label("total_call_count"),
            )
            .where(*filters)
            .group_by(CallForService.year_month, CallForService.agency_name)
            .order_by(CallForService.year_month)
        )
        data = (await sess.execute(query)).all()
    line_data = []

    if data:
        line_data = await format_line_data(data=data)

        
    call_for_service_data = {}
    if line_data:
        call_for_service_data.update({"call_for_service_agency_wide_line": line_data})
    return call_for_service_data


async def get_call_for_service_comment(
    line_name: str, transport_type: str, section_heading: str, year_month, published: bool
):
    comment = ""

    try:
        comment = await AdminReview.get_comment(
            year_month=year_month,
            stat_type=PageType.CALLS_FOR_SERVICE,
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

    filters = [CallForService.published == published]

    if transport_type:
        filters.append(CallForService.transport_type == transport_type)

    async with get_session() as sess:
        query = (
            select(CallForService.year_month)
            .where(*filters)
            .distinct()
            .order_by(CallForService.year_month.desc())
        )
        data = (await sess.scalars(query)).all()
    return data
