URLS = {
    "login": "https://appapi.xueanquan.com/usercenter/api/v3/wx/login?checkShowQrCode=true&tmp=false",
    "sign": "https://huodongapi.xueanquan.com/p/guangdong/Topic/topic/platformapi/api/v1/records/sign",
    "gather": "https://gather.xueanquan.com/",
    "special": "https://file.xueanquan.com/webapi.guangdong/CourseAndSkill/NSpecialList.html",
    "need": "https://huodongapi.xueanquan.com/Topic/topic/main/api/v1/records/special-info?specialId=875&comeFrom=20232&countyId=120021012"
}

PAYLOADS = {
    "login": {
        "username": None,
        "password": None,
        "loginOrigin": 1
    },
    "sign": {
        "specialId": 0,
        "step": 1,
    },
    "gather": [
        {
            "body": None,
            "headers": {
                "topic": "OpenPlatform_Activity_Client"
            }
        }
    ],
    "gather_body": [
        {
            "channel": "01",
            "local_timestamp": None,  # 时间戳
            "client_ip": "",
            "attach": {
                "page_id": None,
                # special-891-navigationbar-1-1
                # 这个是活动页面的标签,位于banner下面,第一位代表的是第一行的标签,第二个为子标签
                # 如果没有子标签,则第一位为0,第二位代替第一位
                # 一开始是抓包推出来的,蠢的很,没想到有对应的js
                # 但是这个id的获取很麻烦,而且也消耗性能,所以我推测了以下几点
                # 学生需要做的通常是 2-1 所以我们只需要默认使用 2-1 即可
                # 但因为某些情况,我也会开一个特例,如0-1,0-2,0-3,这类情况需要自己去手动开启
                # 参考链接:
                # https://file.xueanquan.com/special-system/runtime/dataCollection.js?r=20220301
                # https://file.xueanquan.com/special-system/runtime/test-1.10.2.js?r=20220301
                # https://huodong.xueanquan.com/2023fzjz/style/common.js?r=20230425
                #
                "button_id": None,
                # navigationbar-1-1-done
                "code": None
                # 因为会发送两次请求，所以这里会有所修改
                # 参数 000 200_0 200_1
                # 000是一开始就发送一次,200_0表示签到时出现错误,包括重复签到,200_1表示正常签到成功
            },
            "user": {
                "user_id": None,
                "platform_id": "1001_1",
                "login_type": "account",
                "open_id": "",
                "union_id": "",
                "session_id": ""
            },
            "event": "3003",
            "device": {
                "imei": "",
                "imsi": "",
                "idfa": "",
                "gsm_mac": "",
                "wifi_mac": "",
                "bluetooth_mac": "",
                "android_id": "",
                "device_id": "",
                "device_brand": "",
                "device_model": "",
                "device_resolution": "",
                "os_type": "pc",
                "os_version": ""
            },
            "env": {
                "app_version": "",
                "sdk_version": "",
                "carrier": "",
                "network_type": "",
                "data_type": "release"
            }
        }
    ],
}
