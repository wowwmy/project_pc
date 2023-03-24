import requests


def request():
    url = 'https://weibo.com/ajax/side/hotSearch'
    res = requests.get(url=url).json()
    return res


def search(res):
    data = res['data']
    realtime = data['realtime']
    return realtime


def top(res):
    data = res['data']
    topping = data['hotgov']['word']
    topping_url = data['hotgov']['url']
    return [topping, topping_url]


def hot():
    res = request()
    realtime = search(res)
    tops = top(res)
    print(tops)


hot()
