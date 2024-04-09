import aiohttp
import asyncio

host_url = "http://localhost:5000"
async def register(payload):
    url = f"{host_url}/api/v1/auth/register"
    tasks = []
    tasks.append(test_async_api("POST", url=url, data=payload))
    await asyncio.gather(*tasks, return_exceptions=True)


async def test_async_api(method, url, params=None, data=None, headers=None):
    """
    Test an asynchronous API with the specified method, URL, parameters, data, and headers.

    Args:
        method (str): The HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE').
        url (str): The URL of the API endpoint.
        params (dict, optional): Dictionary of URL parameters.
        data (dict, optional): Dictionary of request body data.
        headers (dict, optional): Dictionary of request headers.

    Returns:
        dict: A dictionary containing the status code and response content.
    """
    async with aiohttp.ClientSession() as session:
        async with getattr(session, method.lower())(
            url, params=params, json=data, headers=headers
        ) as response:
            try:
                response_data = await response.json()
            except aiohttp.ContentTypeError:
                response_data = await response.text()

            print({"url": url, "status_code": response.status, "response": response_data})
            return {"status_code": response.status, "response": response_data}
        

if __name__ == "__main__":
    asyncio.run(register({
        "username": "metro_master",
        "password": "metro_pass",
        "email": "master@metro.com"
    }))