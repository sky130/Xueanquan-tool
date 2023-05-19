from util import login, get_specials, get_homeworks, finish_homeworks, finish_specials

_data = login("test", "test")
finish_homeworks(get_homeworks(data=_data))
finish_specials(get_specials(1, data=_data), _data)
