Xueanquan-tool是一个帮助用户根据需要开发出来的Python工具
它能够更加方便的帮助用户使用少量Python代码完成安全平台任务,但并不保证它能工作
在多数情况下奏效

---

# 使用案例

修改`run.py`内容

```python
from util import login, get_specials, get_homeworks, finish_homeworks, finish_specials

_data = login("username", "password")  # 登录账号密码
finish_homeworks(get_homeworks(data=_data))  # 获取所有作业列表后再完成
finish_specials(get_specials(0, data=_data), _data)  # 获取所有活动列表后再完成

```

运行`main.py`即可

---

# 全部接口

- `login()`：登录到该平台并获取用户数据
- `finish_homework()`：完成作业任务
- `finish_homeworks()`：完成多个作业任务
- `finish_specials()`：完成多个专题任务
- `finish_special()`：完成单个专题任务
- `get_homeworks()`：获取作业列表
- `get_specials()`：获取专题列表

---

# 数据配置

这是`config.py`中的代码

```python
config = {
    "getMoreSpecialPageIds": False,  # 取更多的page-id,如果出问题可以改为True
    "debugInfo": False,  # 调试方式
    "onlyNeedToDo": True,  # 只做该做的,仅在`get_specials()`起效
    "retryTimes": 2,  # 重试次数
}
```

按需求修改
---

# 适配情况

- [x] 获取"我的学习"列表
- [x] 获取"所有活动"列表
- [x] 登录账号
- [x] 完成活动
- [x] 完成作业
