import aiohttp
import asyncio

host_url = "http://localhost:5000"

routes = {
    "crime_ucr": [
        f"{host_url}/crime?transport_type=rail&line_name=A%20Line%20(Blue)&vetted=false&severity=serious_crime"
    ],
    "crime_data": [f"{host_url}/crime/data"],
    "crime_date": [],
    "crime_comment": [],
    "crime_data_agency": [f"{host_url}/crime/data/agency"],
    "routes": [],
    "dashboard": [],
    "arrest_data": [f"{host_url}/arrest/data"],
    "arrest_agency_data": [f"{host_url}/arrest/data/agency"],
    "arrest_comment": [f"{host_url}/arrest/comment"],
    "arrest_date": [
        f"{host_url}/arrest/date_details?published=true&transport_type=bus",
        f"{host_url}/arrest/date_details?published=true",
    ],
    "cfs_data": [f"{host_url}/call_for_service/data"],
    "cfs_agency_data": [f"{host_url}/call_for_service/data/agency"],
    "cfs_comment": [f"{host_url}/call_for_service/comment"],
    "cfs_date": [f"{host_url}/call_for_service/date_details?published=true&transport_type=rail", f"{host_url}/call_for_service/date_details?published=true"]
}

crime_bar = {
    "line_name": "A Line (Blue)",
    "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    "transport_type": "rail",
    "severity": "serious_crime",
    "crime_category": "persons",
    "vetted": True,
    "published": True,
    "graph_type": "bar",
}
crime_line = {
    "line_name": "A Line (Blue)",
    "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    "transport_type": "rail",
    "severity": "serious_crime",
    "crime_category": "persons",
    "vetted": True,
    "published": True,
    "graph_type": "line",
}
crime_comment = {
    "line_name": "A Line (Blue)",
    "transport_type": "rail",
    "vetted": True,
    # "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    "dates": ["2023-11-01"],
    "section": "serious_crime",
    "published": True,
    "crime_category": "persons",
}
arrest_pie = {
    "line_name": "A Line (Blue)",
    "transport_type": "rail",
    "gender": "female",
    "published": True,
    # "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    "dates": ["2024-01-01"],
    "graph_type": "pie",
}
arrest_line = {
    "line_name": "A Line (Blue)",
    "transport_type": "rail",
    "gender": "female",
    "published": True,
    # "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    "dates": ["2024-01-01"],
    "graph_type": "pie",
}
arrest_agency_bar = {
    "line_name": "A Line (Blue)",
    "transport_type": "rail",
    "gender": "female",
    "published": True,
    # "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    "dates": ["2024-01-01"],
    "graph_type": "bar",
}
arrest_agency_line = {
    "line_name": "A Line (Blue)",
    "transport_type": "rail",
    "gender": "female",
    "published": True,
    # "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    "dates": ["2024-01-01"],
    "graph_type": "line",
}
arrest_comment = {
    "line_name": "A Line (Blue)",
    "transport_type": "rail",
    # "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    "dates": ["2023-11-01"],
    "section": "female category",
    "published": True,
}
cfs_data_bar = {
    "line_name": "A Line (Blue)",
    "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    "transport_type": "rail",
    "published": True,
    "graph_type": "bar",    
}
cfs_data_line = {
    "line_name": "A Line (Blue)",
    "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    "transport_type": "rail",
    "published": True,
    "graph_type": "line",    
}
cfs_agency_bar = {
    "line_name": "A Line (Blue)",
    "transport_type": "rail",
    "published": True,
    "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    # "dates": ["2024-01-01"],
    "graph_type": "bar",
}
cfs_agency_line = {
    "line_name": "A Line (Blue)",
    "transport_type": "rail",
    "published": True,
    "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    # "dates": ["2024-01-01"],
    "graph_type": "line",
}
cfs_comment = {
    "line_name": "A Line (Blue)",
    "transport_type": "rail",
    # "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    "dates": ["2023-11-01"],
    "section": "calls_classification",
    "published": True,
}

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


async def main(get_url=None, post_url=None, json_data=None):
    # GET request
    tasks = []
    for x in range(1):
        if post_url:
            tasks.append(test_async_api("POST", url=post_url, data=json_data))

        if get_url:
            tasks.append(test_async_api("GET", get_url))
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    # url = "http://localhost:5001/crime/data/"
    # url = "http://localhost:5001/crime/data/agency"
    # url = "http://localhost:5001/crime/comment"
    post_url = routes["cfs_comment"][0]

    
    # url = "http://localhost:5001//crime/data?line_name=A%20Line%20(Blue)&from_date=2024-01-01&to_date=2024-02-01&severity=serious_crime&crime_category=persons&vetted=true&published=false&graph_type=bar"
    # url = "http://localhost:5001//crime/data?line_name=A%20Line%20(Blue)&from_date=2024-01-01&to_date=2024-02-01&severity=serious_crime&vetted=true&published=false&graph_type=bar"
    # url = "http://localhost:5001//crime/date_details?vetted=true&published=false&transport_type=rail"
    # url = "http://localhost:5001/crime/comment?line_name=A%20Line%20(Blue)&from_date=2023-11-01&to_date=2023-11-30&section=serious_crime&vetted=true&published=false&crime_category=persons&transport_type=rail"
    # url = "http://localhost:5001//crime/data/agency?line_name=A%20Line%20(Blue)&from_date=2024-01-01&to_date=2024-02-01&severity=serious_crime&crime_category=persons&vetted=true&published=false&graph_type=bar"
    # url = "http://localhost:5001//crime/data?line_name=A%20Line%20(Blue)&transport_type=rail&from_date=2024-01-01&to_date=2024-02-01&severity=serious_crime&crime_category=persons&vetted=true&published=false"
    # url = "http://localhost:5001//crime/data?line_name=A%20Line%20(Blue)&transport_type=rail&from_date=2024-01-01&to_date=2024-02-01&severity=serious_crime&crime_category=persons&vetted=false&published=false"
    # url = "http://localhost:5001/dashboard_details?transport_type=rail&published=true"
    # url = "http://localhost:5000/dashboard_details?published=true"
    # url = "http://localhost:5001/routes?stat_type=call_for_services&vetted=true&transport_type=rail"
    # url = "http://localhost:5000/routes?stat_type=crime&vetted=false&transport_type=rail"
    # url = "http://localhost:5000/routes?stat_type=crime&transport_type=rail"
    # url = "http://13.233.193.48:5000/routes?stat_type=arrest&vetted=true&transport_type=rail"
    # url = "http://127.0.0.1:5001/crime?transport_type=rail&line_name=A%20Line%20(Blue)&vetted=false"
    # url = "http://127.0.0.1:5000//crime/data?transport_type=rail&route=route_a&from_date=2023-10&to_date=2023-12&crime_type=person&crime_category=major"
    # asyncio.run(main(post_url=post_url, json_data=cfs_comment))
    asyncio.run(main(get_url=routes["cfs_date"][1]))
