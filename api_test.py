import asyncio

import aiohttp

host_url = "http://localhost:5000"

routes = {
    "crime_ucr": [
        f"{host_url}/crime?transport_type=rail&line_name=A%20Line%20(Blue)&vetted=true&severity=violent_crime",
        f"{host_url}/crime?transport_type=rail&line_name=A%20Line%20(Blue)&vetted=true&severity=systemwide_crime",
        f"{host_url}/crime?transport_type=rail&line_name=A%20Line%20(Blue)&vetted=true",
        f"{host_url}/crime?severity=violent_crime&vetted=false",
    ],
    "crime_data": [f"{host_url}/crime/data"],
    "crime_date": [
        f"{host_url}/crime/date_details?vetted=false&published=true&transport_type=rail",
        f"{host_url}/crime/date_details?vetted=true&published=true&transport_type=rail",
        f"{host_url}/crime/date_details?vetted=false&published=false&transport_type=rail",
        f"{host_url}/crime/date_details?vetted=true&published=false&transport_type=rail",
        f"{host_url}/crime/date_details?vetted=false&published=true&transport_type=bus",
        f"{host_url}/crime/date_details?vetted=true&published=true&transport_type=bus",
        f"{host_url}/crime/date_details?vetted=false&published=false&transport_type=bus",
        f"{host_url}/crime/date_details?vetted=true&published=false&transport_type=bus",
        f"{host_url}/crime/date_details?vetted=false&published=true",
        f"{host_url}/crime/date_details?vetted=false&published=false",
        f"{host_url}/crime/date_details?vetted=true&published=true",
        f"{host_url}/crime/date_details?vetted=true&published=false",
    ],
    "crime_data_agency": [f"{host_url}/crime/data/agency"],
    "crime_comment": [f"{host_url}/crime/comment"],
    "routes": [
        f"{host_url}/routes/?stat_type=calls_for_service&transport_type=rail",
        f"{host_url}/routes/?stat_type=arrest&vetted=false&transport_type=rail",
    ],
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
    "cfs_date": [
        f"{host_url}/call_for_service/date_details?published=true&transport_type=rail",
        f"{host_url}/call_for_service/date_details?published=true",
    ],
}

crime_bar = [
    {
        "line_name": "A Line (Blue)",
        "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
        "transport_type": "rail",
        "severity": "systemwide_crime",
        "crime_category": "persons",
        "vetted": True,
        "published": True,
        "graph_type": "bar",
    },
    {
        "line_name": "A Line (Blue)",
        "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
        "transport_type": "rail",
        "severity": "violent_crime",
        "crime_category": "persons",
        "vetted": True,
        "published": True,
        "graph_type": "bar",
    },
    {
        "line_name": "A Line (Blue)",
        "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
        "transport_type": "rail",
        "severity": "violent_crime",
        "crime_category": "",
        "vetted": True,
        "published": True,
        "graph_type": "bar",
    },
    {
        "line_name": "A Line (Blue)",
        "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
        "transport_type": "rail",
        "severity": "violent_crime",
        "vetted": True,
        "published": True,
        "graph_type": "bar",
    },
    {
        "line_name": "A Line (Blue)",
        "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
        "transport_type": "rail",
        "severity": "systemwide_crime",
        "crime_category": "",
        "vetted": True,
        "published": True,
        "graph_type": "bar",
    },
    {
        "line_name": "A Line (Blue)",
        "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
        "transport_type": "rail",
        "severity": "systemwide_crime",
        "vetted": True,
        "published": True,
        "graph_type": "bar",
    },
]
crime_line = {
    "line_name": "K Line",
    # "line_name": "A Line (Blue)",
    "dates": ["2024-01-01"],
    # "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    "transport_type": "rail",
    "severity": "systemwide_crime",
    # "severity": "violent_crime",
    "crime_category": "persons",
    "vetted": False,
    "published": True,
    "graph_type": "bar",
    # "graph_type": "line",
}
crime_agency_bar = {
    "line_name": "A Line (Blue)",
    "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    "transport_type": "rail",
    "crime_category": "persons",
    "vetted": True,
    "published": True,
    "graph_type": "bar",
}
crime_agency_line = {
    "line_name": "A Line (Blue)",
    "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    "transport_type": "rail",
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
    "section": "systemwide_crime",
    "published": True,
    "crime_category": "all",
}
arrest_pie = {
    # "line_name": "A Line (Blue)",
    # "transport_type": "rail",
    "gender": "male",
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
    "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    # "dates": ["2024-01-01"],
    "graph_type": "line",
}
arrest_agency_bar = {
    "line_name": "A Line (Blue)",
    "transport_type": "rail",
    "published": True,
    # "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    "dates": ["2024-01-01"],
    "graph_type": "bar",
}
arrest_agency_line = {
    "line_name": "A Line (Blue)",
    "transport_type": "rail",
    "published": True,
    "dates": ["2024-01-01", "2023-12-1", "2023-10-1"],
    # "dates": ["2024-01-01"],
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
    "line_name": None,
    # "line_name": "A Line (Blue)",
    "transport_type": "systemwide",
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

            print({"url": url, "status_code": response.status, "response": response_data})
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


async def run_multiple_get(url_list):
    # GET request
    tasks = []
    for url in url_list:
        tasks.append(test_async_api("GET", url))
    await asyncio.gather(*tasks, return_exceptions=True)


async def run_multiple_post(url_data_list):
    tasks = []
    for url, json_data in url_data_list:
        tasks.append(test_async_api("POST", url=url, data=json_data))
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":

    post_url = routes["arrest_data"][0]
    # asyncio.run(main(post_url=post_url, json_data=arrest_pie))

    asyncio.run(main(get_url=routes["crime_ucr"][3]))
    # asyncio.run(run_multiple_get(routes["crime_date"]))

    # url_data_list = []
    # for x in crime_bar:
    # url_data_list.append((routes["crime_data"][0], x))

    # asyncio.run(run_multiple_post(url_data_list))
