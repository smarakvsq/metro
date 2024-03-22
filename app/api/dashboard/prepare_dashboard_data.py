from app.db import get_session
from app.models import CallsForServiceLanding, CrimeLanding, ArrestLanding, AdminReview

from sqlalchemy import select


async def get_call_for_service_data(transport_type: str, published: bool):
    comment = ""
    async with get_session() as sess:
        data: CallsForServiceLanding = (
            await sess.scalars(
                select(CallsForServiceLanding)
                .where(
                    CallsForServiceLanding.transport_type == transport_type,
                    CallsForServiceLanding.published == published,
                )
                .order_by(CallsForServiceLanding.current_year_month.desc())
            )
        ).first()

    if data:
        comment = await AdminReview.get_comment(admin_id=data.admin_review_id)

    call_for_service_data = data.to_json()
    call_for_service_data.update({"comment": comment})
    return call_for_service_data


async def get_crime_data(transport_type: str, published: bool):
    comment = ""
    async with get_session() as sess:
        data: CrimeLanding = (
            await sess.scalars(
                select(CrimeLanding)
                .where(
                    CrimeLanding.transport_type == transport_type,
                    CrimeLanding.published == published,
                )
                .order_by(CrimeLanding.current_year_month.desc())
            )
        ).first()

    if data:
        comment = await AdminReview.get_comment(admin_id=data.admin_review_id)

    crime_data = data.to_json()
    crime_data.update({"comment": comment})
    return crime_data


async def get_arrest_data(transport_type: str, published: bool):
    comment = ""
    async with get_session() as sess:
        data = (
            await sess.scalars(
                select(ArrestLanding)
                .where(
                    ArrestLanding.transport_type == transport_type,
                    ArrestLanding.published == published,
                )
                .order_by(ArrestLanding.current_year_month.desc())
            )
        ).first()

    if data:
        comment = await AdminReview.get_comment(admin_id=data.admin_review_id)

    arrest_data = data.to_json()
    arrest_data.update({"comment": comment})
    return arrest_data
