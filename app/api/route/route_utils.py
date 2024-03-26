from app.db import get_session
from sqlalchemy import select
from app.models import CrimeVetted, CrimeUnvetted, Arrest, CallForService


async def select_crime_table(vetted: bool):
    return CrimeVetted if vetted else CrimeUnvetted


async def select_stat_table(stat_type: str, vetted: bool):
    mapper = {
        "crime": await select_crime_table(vetted=vetted),
        "arrest": Arrest,
        "call_for_service": CallForService
    }
    stat_type = stat_type.lower()
    return mapper[stat_type]


async def get_unique_lines(stat_type: str, vetted: bool, transport_type: str):
    data = []
    Table = await select_stat_table(stat_type, vetted)
    async with get_session() as sess:
        data = (
            await sess.scalars(
                select(Table.line_name).where(Table.transport_type==transport_type).distinct()
            )
        ).all()

    return data