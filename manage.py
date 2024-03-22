from app import metro_app

if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(metro_app.run(debug=True))
