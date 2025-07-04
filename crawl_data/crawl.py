import requests
import json

def  get_token():
    url = "https://gw.be.com.vn/api/v1/be-delivery-gateway/api/v1/user/guest"

    payload = json.dumps({
    "locale": "vi",
    "app_version": "11280",
    "version": "1.1.280",
    "device_type": 3,
    "operator_token": "0b28e008bc323838f5ec84f718ef11e6",
    "customer_package_name": "xyz.be.food",
    "device_token": "",
    "ad_id": "",
    "screen_width": 360,
    "screen_height": 640,
    "access_token": "PENDING",
    "client_info": {
        "locale": "vi",
        "app_version": "11280",
        "version": "1.1.280",
        "device_type": 3,
        "operator_token": "0b28e008bc323838f5ec84f718ef11e6",
        "customer_package_name": "xyz.be.food",
        "device_token": "",
        "ad_id": "",
        "screen_width": 360,
        "screen_height": 640,
        "access_token": "PENDING"
    },
    "latitude": None,
    "longitude": None
    })
    headers = {
    'accept': '*/*',
    'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'access_token': 'PENDING',
    'app_version': '11280',
    'content-type': 'application/json',
    'origin': 'https://food.be.com.vn',
    'priority': 'u=1, i',
    'referer': 'https://food.be.com.vn/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)["access_token"]


def get_restaurent(page, latitude, longitude):

    access_token = get_token()

    url = "https://gw.be.com.vn/api/v1/be-marketplace/web/collection/items/restaurants"
    payload = json.dumps({
    "collection_id": "231",
    "page": page,
    "filters": [],
    "limit": 100,
    "locale": "vi",
    "app_version": "11280",
    "version": "1.1.280",
    "device_type": 3,
    "operator_token": "0b28e008bc323838f5ec84f718ef11e6",
    "customer_package_name": "xyz.be.food",
    "device_token": "43be67cda697604c0781023d055ef5d7",
    "ad_id": "",
    "screen_width": 360,
    "screen_height": 640,
    "client_info": {
        "locale": "vi",
        "app_version": "11280",
        "version": "1.1.280",
        "device_type": 3,
        "operator_token": "0b28e008bc323838f5ec84f718ef11e6",
        "customer_package_name": "xyz.be.food",
        "device_token": "43be67cda697604c0781023d055ef5d7",
        "ad_id": "",
        "screen_width": 360,
        "screen_height": 640
    },
    "latitude": latitude,
    "longitude": longitude
    })
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/json',
    'Referer': 'https://food.be.com.vn/',
    'app_version': '11280',
    'version': '1.1.280',
    'Origin': 'https://food.be.com.vn',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Authorization': f'Bearer {access_token}',
    'Connection': 'keep-alive',
    'TE': 'trailers'
    }

    return requests.request("POST", url, data=payload, headers= headers).text

data_response = json.loads(get_restaurent(page = 1,latitude=10.826233309253325,longitude=106.62746414326836))
print(data_response)
