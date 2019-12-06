from django.test import TestCase
import requests
import random
from faker import Faker

base_url = 'http://127.0.0.1:8000/device_manage/'


def get_status():
    data = {'type': 'tool'}
    response = requests.post(f'{base_url}status/', json=data)
    print(response.json())


def create_data(num):
    for i in range(num):
        fake = Faker(locale='zh_CN')
        data = {
            "device_ip": f"203.1.4.{random.randint(1, 255)}",
            "device_name": fake.name(),
            "device_version": fake.word(),
            "tool_ip": f"203.1.4.{random.randint(1, 255)}",
            "tool_pc_ip": "203.1.4.12",
            "sd_status": 0,
            "address": '浙江杭州'
        }
        response = requests.post(url=base_url, json=data)
        print(response.json())


if __name__ == '__main__':
    # create_data(30)
    get_status()
