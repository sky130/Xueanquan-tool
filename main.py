import requests

from config import config

while True:
    time = 0
    try:
        import run
    except requests.exceptions.ConnectionError as e:
        print("出现错误,正在重试")
        time += 1
        if time > config["retryTimes"]:
            print(e)
            break
        continue
    break
