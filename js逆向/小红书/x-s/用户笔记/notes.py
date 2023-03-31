import requests
import execjs
import urllib.parse


class Notes:
    def __init__(self):
        with open('x-s.js', 'r', encoding='utf-8') as f:
            self.js_text = execjs.compile(f.read())

    def get_xsxt(self, l):
        params = self.js_text.call('sign', l)
        s = params['X-s']
        t = params['X-t']
        return s, t

    def request(self, uid):
        url = 'https://edith.xiaohongshu.com/api/sns/web/v1/user_posted'
        params = {
            "num": "30",
            "cursor": "",
            "user_id": uid
        }
        l = '/api/sns/web/v1/user_posted' + '?' + urllib.parse.urlencode(params)
        s, t = self.get_xsxt(l)
        params = {
            "num": "30",
            "cursor": "",
            "user_id": uid
        }

        headers = {
            "cookie": "web_session=030037a311bc0245f9733aae5a234abc1ef050",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "x-s": s,
            "x-t": f"{t}"
        }
        res = requests.get(url=url, params=params, headers=headers).json()
        print(res)

    def run(self):
        uids = ['61ac48c600000000210200fe']
        for uid in uids:
            self.request(uid)


if __name__ == '__main__':
    Notes().run()
