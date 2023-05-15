import json
import re
import time

import requests
from bs4 import BeautifulSoup

from config import config
from urls import *


class LinkData:
    def __init__(self, link, name, _id):
        self.link = link
        self.name = name
        self.id = _id


class UserData:
    def __init__(self, cookies, response_json: json):
        self.cookies = cookies
        self.user_id = response_json['data']['userId']
        self.host = response_json['data']['serverSide']
        self.come_from = response_json['data']['comeFrom']
        self.is_weak_pwd = response_json['data']['isWeakPwd']


class FinishData:
    def __init__(self, response_json: json):
        self.result = response_json["result"]
        self.msg = response_json["msg"]
        self.http_code = response_json["httpCode"]


def get_specials(size=10, needs_verify=True, host="https://maoming.xueanquan.com"):
    url = f'{URLS["special"]}?pagesize={size}&key=&host={host}'
    response = requests.get(url, timeout=10)
    return parse_html_code(response.text, needs_verify)


def get_id(url):
    response = requests.get(url + "message.html")
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string
    return title


def parse_js_code(js_code):
    a = ""
    pattern = r'document\.writeln\(\'(.+?)\'\);'
    matches = re.findall(pattern, js_code)
    for match in matches:
        a = a + str(match) + "\n"
    return a


def parse_html_code(code: str, needs_verify=True):
    name = []
    url = []
    data = []
    soup = BeautifulSoup(parse_js_code(code), features="html.parser")
    divs = soup.find_all('div', class_='headb')
    for div in divs:
        name.append(div.text.strip().split("：")[1])

    divs = soup.find_all('div', class_='seminar_box')
    for div in divs:
        url.append(str(div.find('a')['href']))
    for i in range(len(name)):
        if "require-un=true" in url[i] or not needs_verify:  # 判断是否必做
            _url = url[i].replace("?require-un=true", "").replace("index.html", "")
            _id = get_id(_url)
            if _id == "404 Not Found":
                continue
            data.append(LinkData(_url, name[i], _id))
    return data


def login(username, password):
    payloads = PAYLOADS["login"]
    payloads["username"] = username
    payloads["password"] = password
    response = requests.post(URLS["login"], json=payloads, timeout=10)
    if response.status_code == 200:
        err_code = response.json()["err_code"]
        if err_code != 0:
            print("出现报错,错误码为", err_code, ",报错反馈如下")
            print(response.json()["err_desc"])
            return
        data = UserData(response.cookies, response.json())
        if data.is_weak_pwd == "false":
            return
        return data
    return


def finish_specials(specials: list[LinkData], data: UserData):
    if data is None:
        print("用户数据为空,未登录成功")
        return
    data_list = list[FinishData]()
    for special in specials:
        fd = finish_special(data, special)
        if fd.http_code == 200:
            data_list.append(fd)
    return data_list


def finish_special(data: UserData, link_data: LinkData = None, id: int = None):
    payload = PAYLOADS["sign"]
    if id is None and LinkData is not None:
        payload["specialId"] = link_data.id
    elif id is not None and LinkData is None:
        payload["specialId"] = id
    elif id is None and LinkData is None:
        payload["specialId"] = link_data.id
    else:
        return
    timestamp = int(time.time() * 1000)
    gather(data, payload["specialId"], "000", timestamp)
    response = requests.post(URLS["sign"], json=payload, cookies=data.cookies, timeout=10)
    fd = FinishData(response.json())
    if fd.result == "true":
        gather(data, payload["specialId"], "200_1", timestamp)
    else:
        gather(data, payload["specialId"], "200_0", timestamp)
    print(fd.msg)
    return fd


def get_special_page_id(id: int):
    if not config["getMoreSpecialPageIds"]:
        return f"special-{id}-navigationbar-2-1"
    else:
        return [f"special-{id}-navigationbar-0-1", f"special-{id}-navigationbar-0-2", f"special-{id}-navigationbar-0-3"]


def get_special_button_id(id: int):
    if not config["getMoreSpecialPageIds"]:
        return f"{id}-navigationbar-2-1"
    else:
        return [f"{id}-navigationbar-0-1", f"{id}-navigationbar-0-2", f"{id}-navigationbar-0-3"]


def gather(data: UserData, id: int, code: str, timestamp: int):
    gather_body = PAYLOADS["gather_body"]
    gather_body[0]["local_timestamp"] = timestamp
    gather_body[0]["user"]["user_id"] = data.user_id
    gather_body[0]["attach"]["page_id"] = get_special_page_id(id)
    gather_body[0]["attach"]["button_id"] = get_special_button_id(id)
    gather_body[0]["attach"]["code"] = code
    payload = PAYLOADS["gather"]
    payload[0]["body"] = json.dumps(gather_body)
    requests.post(URLS["gather"], cookies=data.cookies, json=payload)
