from app import metro_app
import asyncio


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(metro_app.run(host="0.0.0.0", debug=True))
    except KeyboardInterrupt:
        print("Stopping web server")
    finally:
        loop.close()
