from flask import jsonify
from sqlalchemy import select

from app.constants import PageType
from app.db import get_session
from app.models import Arrest, CallForService
from app.util import select_crime_table


async def select_stat_table(stat_type: str, vetted: bool):
    mapper = {
        PageType.CRIME: await select_crime_table(vetted=vetted),
        PageType.ARREST: Arrest,
        PageType.CALLS_FOR_SERVICE: CallForService,
    }
    stat_type = stat_type.lower()
    return mapper[stat_type]


async def get_unique_lines(stat_type: str, vetted: bool, transport_type: str):

    data = []

    if (stat_type == PageType.CRIME) and (vetted is None):
        return {"Error": f"vetted required for type {stat_type}"}

    Table = await select_stat_table(stat_type, vetted)
    async with get_session() as sess:
        data = (
            await sess.scalars(
                select(Table.line_name).where(Table.transport_type == transport_type).distinct()
            )
        ).all()

    return data
