from django.test import TestCase
import requests
import random
from faker import Faker

base_url = 'http://127.0.0.1:8000/device_manage/'


def get_status(type=1):
    if type == 1:
        data = {'device_ip': '203.1.4.10'}
    elif type == 2:
        data = {'device_name': 'abc'}
    elif type == 3:
        data = {'type': 'daily'}
    elif type == 4:
        data = {'type': 'tool'}
    elif type == 5:
        data = {'type': 'unuse'}
    else:
        data = {}
    response = requests.post(f'{base_url}status/', json=data)
    print(response.json())


def use(use_status=1):
    data = {
        'device_ip': '203.1.4.10',
        'use_status': use_status,
        'daily_status': 0
    }
    response = requests.post(f'{base_url}use/', json=data)
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
    # create_data(1)
    get_status(type=1)
    get_status(type=2)
    get_status(type=3)
    get_status(type=4)
    get_status(type=5)
    use(use_status=0)
    use(use_status=1)
    use(use_status='123')
