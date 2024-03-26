import aiohttp
import asyncio


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

            print({"status_code": response.status, "response": response_data})
            return {"status_code": response.status, "response": response_data}


async def main(get_url=None, post_url=None):
    # GET request
    tasks = []
    for x in range(1): 
        tasks.append(test_async_api("GET", get_url))
    await asyncio.gather(*tasks, return_exceptions=True)
    

if __name__ == "__main__":
    # url = "http://localhost:5000/dashboard_details?transport_type=Rail&published=true"
    url = "http://localhost:5000/dashboard_details?published=true"
    # url = "http://localhost:5000/routes?stat_type=arrest&vetted=true"
    # url = "http://127.0.0.1:5000/routes?type=crime&transport_type=rail"
    # url = "http://127.0.0.1:5000/crime?transport_type=rail&route=route_a"
    # url = "http://127.0.0.1:5000//crime/data?transport_type=rail&route=route_a&from_date=2023-10&to_date=2023-12&crime_type=person&crime_category=major"
    asyncio.run(main(get_url=url))
