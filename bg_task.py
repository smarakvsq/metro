# app.py
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.tasks import update_aggregation_tables


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        scheduler = AsyncIOScheduler()
        scheduler.add_job(update_aggregation_tables, "interval", hours=6)
        scheduler.start()
        loop.run_forever()
    except KeyboardInterrupt:
        print("Stopping web server")
    finally:
        loop.close()
