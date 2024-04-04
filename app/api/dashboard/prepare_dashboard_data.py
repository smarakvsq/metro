from sqlalchemy import select

from app.constants import TransportType
from app.db import get_session
from app.models import AdminReview, ArrestLanding, CallsForServiceLanding, CrimeLanding


async def get_call_for_service_data(transport_type: str, published: bool):
    comment = ""
    data = None
    conditions = []

    if transport_type:
        conditions.append(CallsForServiceLanding.transport_type == transport_type)
    else:
        conditions.append(CallsForServiceLanding.transport_type == TransportType.SYSTEM_WIDE)

    if published:
        conditions.append(CallsForServiceLanding.published == published)

    async with get_session() as sess:
        data: CallsForServiceLanding = (
            await sess.scalars(
                select(CallsForServiceLanding)
                .where(*conditions)
                .order_by(CallsForServiceLanding.current_year_month.desc())
            )
        ).first()

    call_for_service_data = {}
    if data:
        comment = await AdminReview.get_comment_by_id(admin_id=data.admin_review_id)
        call_for_service_data = data.to_json()
        call_for_service_data.update({"comment": comment})
    return call_for_service_data


async def get_crime_data(transport_type: str, published: bool):
    comment = ""
    data = None
    conditions = []

    if transport_type:
        conditions.append(CrimeLanding.transport_type == transport_type)
    else:
        conditions.append(CrimeLanding.transport_type == TransportType.SYSTEM_WIDE)

    if published:
        conditions.append(CrimeLanding.published == published)

    async with get_session() as sess:
        data: CrimeLanding = (
            await sess.scalars(
                select(CrimeLanding)
                .where(*conditions)
                .order_by(CrimeLanding.current_year_month.desc())
            )
        ).first()

    crime_data = {}
    if data:
        comment = await AdminReview.get_comment_by_id(admin_id=data.admin_review_id)
        crime_data = data.to_json()
        crime_data.update({"comment": comment})
    return crime_data


async def get_arrest_data(transport_type: str, published: bool):
    comment = ""
    data = None
    conditions = []

    if transport_type:
        conditions.append(ArrestLanding.transport_type == transport_type)
    else:
        conditions.append(ArrestLanding.transport_type == TransportType.SYSTEM_WIDE)

    if published:
        conditions.append(ArrestLanding.published == published)

    async with get_session() as sess:
        data = (
            await sess.scalars(
                select(ArrestLanding)
                .where(*conditions)
                .order_by(ArrestLanding.current_year_month.desc())
            )
        ).first()
    arrest_data = {}
    if data:
        comment = await AdminReview.get_comment_by_id(admin_id=data.admin_review_id)
        arrest_data = data.to_json()
        arrest_data.update({"comment": comment})

    return arrest_data
