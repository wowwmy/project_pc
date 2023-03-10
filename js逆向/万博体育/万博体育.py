import requests,ddddocr

class WBTY:
    def __init__(self):
        self.yzm_url = 'https://cn.fawmx.com/service/verifycode?x=0.6368918535212413'
        self.get_picture()
        self.ocr = ddddocr.DdddOcr()
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "cn.fawmx.com",
            "Origin": "https://cn.fawmx.com",
            "Pragma": "no-cache",
            "Referer": "https://cn.fawmx.com/home/register",
            "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

    def get_picture(self):
        res = requests.get(url=self.yzm_url)
        with open('./yzm.png','wb') as f:
            f.write(res.content)
        return res.cookies

    def ocr_picture(self):
        with open('./yzm.png','rb') as f:
            picture = f.read()
        yzm = self.ocr.classification(picture)
        return yzm

    def get_fkey_cookie(self,cookies):
        url = 'https://cn.fawmx.com/service/vpkey'
        res = requests.get(url=url,headers=self.headers,cookies=cookies)
        print(res.text)
        return res.cookies


    def get_fkey(self,cookie,username):
        url = 'https://cn.fawmx.com/ee/loginverification'
        data = {
            "eeblackbox": "0002MDAwN0xTVE9LRU4wMDI0ZmI5ZGYzZjktZTUxMS00ZTBlLTgzODctNjI0NTQ1OTkzOTBkMDAwNklOVExPQzAwMjJodHRwczovL2NuLmZhd214LmNvbS9ob21lL3JlZ2lzdGVyMDAwN1BSSVZBVEUwMDA1ZmFsc2UwMDA1SkVOQkwwMDAxMTAwMDVKU1NSQzAwMjBodHRwczovL3d3dy5mNGJ6eXJ6OTJ1czMuY29tL0UyLzAwMDRVQUdUMDA2Zk1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMDMuMC4wLjAgU2FmYXJpLzUzNy4zNjAwMDdKU1RPS0VOMDAyNGZiOWRmM2Y5LWU1MTEtNGUwZS04Mzg3LTYyNDU0NTk5MzkwZDAwMDdIQUNDTE5HMDAwZXpoLUNOLHpoO3E9MC45MDAwN0hBQ0NDSFIwMDBmVW5pY29kZSAoVVRGLTgpMDAwNUpTVkVSMDAwMzIuMDAwMDRUWk9OMDAwNC00ODAwMDA2SlNUSU1FMDAxNzIwMjIvMDgvMTUgMDg6NTc6NDMuODAzMDAwN1NWUlRJTUUwMDE0OC8xNS8yMDIyIDg6NTc6NDMgQU0wMDA1SkJSTk0wMDA2Q2hyb21lMDAwNUpCUlZSMDAwOTEwMy4wLjAuMDAwMDVKQlJPUzAwMGZXaW5kb3dzIE5UIDEwLjAwMDA1SkJSQ00wMDFkV2luNjQ7IHg2NDsgS0hUTUwsIGxpa2UgR2Vja28wMDA1SkxBTkcwMDA1emgtQ04wMDA0SlJFUzAwMDg4NjR4MTUzNjAwMDZKUExHTlMwMDY0aW50ZXJuYWwtcGRmLXZpZXdlcjtpbnRlcm5hbC1wZGYtdmlld2VyO2ludGVybmFsLXBkZi12aWV3ZXI7aW50ZXJuYWwtcGRmLXZpZXdlcjtpbnRlcm5hbC1wZGYtdmlld2VyOzAwMDRJR0dZMDAyY3ZPbEpXU2xhckRCbFdFWUpCTnkwc3BuWk1yLzBYSm94a1I2WEJHSmJOZ3c9MDAwNUFQVkVSMDA2NzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTAzLjAuMC4wIFNhZmFyaS81MzcuMzYwMDA1QVBOQU0wMDA4TmV0c2NhcGUwMDA1TlBMQVQwMDA1V2luMzIwMDAyTVYwMDIwRUMxMzU0MkZGM0JBRDk3Q0QzNTJCM0NEODAyODI1NTMwMDAzRVRUMDA1OGJpM3NKZE9lZURyNTMrKzB2L2ZtTmE4WTcxaDQwNlo2SzgwUjluemM0em5mR3lTRVNwa2F0NE9ZbFNDMFdoOGp0SEJrRk5abytpY3VuYXFaOVZhOGhRPT0wMDA0RVRQVDAwNTgrell0NkF3QzN2RGNCakQ1SHJHaUpDSTM1b0hTa0VjTUxiTk9zQVNxM2l0cElReDQzZmVnZUVYTDlTZUhSS08vZi9Sc2Fad01NYWNScVpybjkyY0VBZz09MDAwOFdEQlRPS0VOMDAyNGZiOWRmM2Y5LWU1MTEtNGUwZS04Mzg3LTYyNDU0NTk5MzkwZDAwMDhXRUJSVENJUDAwMGUxMTMuNjUuMjA3LjE4NzAwMDZDVE9LRU4wMDI0ZmI5ZGYzZjktZTUxMS00ZTBlLTgzODctNjI0NTQ1OTkzOTBk",
            "info": f"{username}",
            "p": "",
            "fkey": "0"
        }
        fkey = requests.post(url=url,headers=self.headers,cookies=cookie,data=data).json()
        print(fkey.get('response'))
        return fkey.get('response')

    def get_pwd(self,pwd):
        data = {
            "group":"wbty",
            "action":"login",
            "pwd":f"{pwd}"
        }
        res = requests.get(url="http://127.0.0.1:5620/business-demo/invoke", params=data)
        print(res.json().get('data'))
        return res.json().get('data')

    def login(self,cookies,yzm,fkey,pwd,username):
        url = 'https://cn.fawmx.com/kz/member/loginAdvance?r=0.5195951539991481'
        data = {
            "loginpwd": pwd,
            "loginame": username,
            "verifycode": yzm,
            "fkey": fkey,
            "captchaMethod": "0",
            "captchaToken": "",
            "loginMethod": "0"
        }
        res = requests.post(url=url,headers=self.headers,cookies=cookies,data=data)
        print(res.text)
        return res.cookies

    def run(self,username,pwds):
        cookies = self.get_picture()
        cookie = self.get_fkey_cookie(cookies)
        cookies = dict(cookies)
        cookies['JSESSIONID'] = cookie['JSESSIONID']
        yzm = self.ocr_picture()
        print(yzm)
        fkey = self.get_fkey(cookies,username)
        pwd = self.get_pwd(pwds)
        self.login(cookies,yzm,fkey,pwd,username)


if __name__ == '__main__':
    WBTY().run('账号','密码')
