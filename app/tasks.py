from app.db import get_session  # Import async session function
from app.models import (AdminReview, Arrest, ArrestLanding, CallForService,
                        CallsForServiceLanding, CrimeLanding, CrimeUnvetted,
                        CrimeVetted, Location, RidersSummary)


async def update_aggregation_tables():
    # async with get_session() as session:
    #     # ... your aggregation logic using models ...
    #     pass
    print("hello world")
