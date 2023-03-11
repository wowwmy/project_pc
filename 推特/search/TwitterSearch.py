import requests
from openpyxl import Workbook
import sys


class TTS:
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.create_sheet(title='Twitter', index=0)
        self.ws.append(['id_str', 'name', 'screen_name', 'location'])

    @staticmethod
    def proxies():
        proxies = {
            'https': 'http://127.0.0.1:10809', 'http': 'http://127.0.0.1:10809'
        }
        return proxies

    @staticmethod
    def get_token():
        url = 'https://api.twitter.com/1.1/guest/activate.json'
        headers = {
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        }
        res = requests.post(url=url, proxies=TTS.proxies(), headers=headers).json()
        return res['guest_token']

    def search(self, key):
        url = 'https://api.twitter.com/1.1/search/typeahead.json'
        headers = {
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "origin": "https://twitter.com",
            "referer": "https://twitter.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "x-guest-token": TTS.get_token(),
            "x-twitter-active-user": "yes",
            "x-twitter-client-language": "zh-cn"
        }
        params = {
            "include_ext_is_blue_verified": "1",
            "include_ext_verified_type": "1",
            "q": f"{key}",
            "src": "search_box",
            "result_type": "events,users,topics"
        }
        res = requests.get(url=url, headers=headers, params=params, proxies=TTS.proxies())
        return res

    def parse(self, data):
        user_list = data['users']
        for user in user_list:
            id_str = user['id_str']
            screen_name = user['screen_name']
            name = user['name']
            location = user['location']
            self.save(id_str, name, screen_name, location)

    def save(self, id_str, name, screen_name, location):
        self.ws.append([id_str, name, screen_name, location])

    def run(self):
        keys = ['Huawei']
        for key in keys:
            res = self.search(key)
            self.parse(res.json())
        self.wb.save('./Twitter.xlsx')


if __name__ == '__main__':
    TTS().run()
