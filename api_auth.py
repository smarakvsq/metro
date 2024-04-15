import asyncio

import aiohttp
import requests

host_url = "http://localhost:5000"
login_url = f"{host_url}/api/v1/auth/login"
logout_url = f"{host_url}/api/v1/auth/logout"
landing_url = f"{host_url}/dashboard/comments"


register_payload = {
    "username": "metro_master",
    "password": "metro_pass",
    "email": "master@metro.com",
}

login_payload = {
    "username": "metro_master",
    "password": "metro_pass",
}

logout_payload = {"uid": ""}


def login_logout():
    with requests.Session() as sess:
        resp = sess.post(url=login_url, json=login_payload)
        if resp.status_code == 200:
            print(resp.json())
        else:
            print(resp.status_code, resp.json())
        resp_json = resp.json()
        uid = resp_json.get("uid")

    landing_payload = {"uid": uid}
    with requests.Session() as sess:
        resp = sess.post(url=landing_url, json=landing_payload)
        print(resp.status_code)
        # logout_payload["uid"] = uid
        # logout_resp = sess.post(url=logout_url, json=logout_payload)
        # print(logout_resp.status_code, logout_resp.json())


async def register(payload):
    url = f"{host_url}/api/v1/auth/register"
    tasks = []
    tasks.append(test_register("POST", url=url, data=payload))
    await asyncio.gather(*tasks, return_exceptions=True)


# async def login_logout():
#     async with aiohttp.ClientSession() as session:
#         print(await login(session))
#         # Now you can use the session.uid variable in other parts of your code
#         # ...
#         # print("between login and logout", await session.get("uid"))
#         await logout(session)


# async def login(session):
#     async with session.post(login_url, json=login_payload) as resp:
#         if resp.status == 200:
#             data = await resp.json()
#             print(data)
#             uid = session.cookie_jar.filter_cookies(login_url).get('uid')
#             print(uid)
#             return
#         else:
#             error = await resp.json()
#             print(f'Login failed: {error["error"]}')
#             return

# async def logout(session):
#     async with session.get(f"{host_url}/api/v1/auth/logout") as resp:
#         uid = session.cookie_jar.filter_cookies(login_url).get('uid')
#         print("in logout", uid)
#         if resp.status == 200:
#             data = await resp.json()
#             print(data['message'])
#             print(session.get("uid"))
#         else:
#             error = await resp.json()
#             print(f'Logout failed: {error["error"]}')


async def test_register(method, url, params=None, data=None, headers=None):
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
    # asyncio.run(register(register_payload))
    # asyncio.run(login_logout())
    login_logout()
