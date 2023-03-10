
'''

password: rJMc0AFs2rrYVeGvBgw9XA==
comParam_seqCode: 02CCCBE4D12B379154240CABDB12C083
comParam_signature: f924093e145753fd4e83a15b876dfd90
x-riskdevicesign: e64db075fd06dda7f86653a9c2aafe2d

'''

import execjs,requests

class Login:
    def __init__(self):
        self.user = '账号'
        self.pwd = '密码'

    def get_pwd(self):
        with open('tyypwd.js','r',encoding='utf-8') as f:
            js_txt = f.read()
        pwds = execjs.compile(js_txt).call('pwd',self.pwd,self.user)
        return pwds

    def get_param(self):
        pwds = self.get_pwd()
        with open('tyy_other.js','r',encoding='utf-8') as f:
            js_txt = f.read()
        param = {'userName':self.user,'password':pwds,'referrer':'wap'}
        params = execjs.compile(js_txt).call('get_other',param)
        # print(params)
        return params


    def spider(self):
        params = self.get_param()
        pwd = params.get('password').replace('+','%2B').replace('=','%3D')
        headers ={
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            # "Cookie": "",
            "Host": "m.ctyun.cn",
            "Referer": "https://m.ctyun.cn/wap/main/auth/login?redirect=%2Fmy",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"100\", \"Google Chrome\";v=\"100\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
            "x-riskdevicesign": "e64db075fd06dda7f86653a9c2aafe2d"
        }
        url = f'https://m.ctyun.cn/account/login?userName={params["userName"]}&password={pwd}&referrer=wap&mainVersion=300031500&comParam_curTime={params["comParam_curTime"]}&comParam_seqCode={params["comParam_seqCode"]}&comParam_signature={params["comParam_signature"]}&isCheck=true&locale=zh-cn'
        res1 = requests.get(url,headers=headers)
        print(res1.status_code)
        print(res1.text)

    def run(self):
        self.spider()

if __name__ == '__main__':
    Login().run()