import json
import time
import random
import asyncio
import aiohttp


#ham get token access de crawl du lieu befood
async def get_token(session):
    url = "https://gw.be.com.vn/api/v1/be-delivery-gateway/api/v1/user/guest"

    payload = {
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
    }

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

    async with session.post(url, headers = headers, json = payload) as response:
        data = await response.json()
    return data["access_token"]

async def get_detail_restaurants(restaurant_id, access_token, session):

    url = "https://gw.be.com.vn/api/v1/be-marketplace/web/restaurant/detail"

    payload = {
    "restaurant_id": restaurant_id,
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
    "longitude":	106.704408,
    "latitude":10.775709
    }

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

    async with session.post(url, headers=headers, json = payload) as respponse :
        return await respponse.json()
    
async def main():
    async with aiohttp.ClientSession() as session:
        print(await get_detail_restaurants("31070", await get_token(session),session))

if __name__ == "__main__":
    asyncio.run(main())