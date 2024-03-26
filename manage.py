from app import metro_app

if __name__ == "__main__":
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(metro_app.run(host="0.0.0.0", port=5000, debug=True))
