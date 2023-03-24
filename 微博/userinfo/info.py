import requests
from head import headers
import time, random
import re
import logging
import openpyxl
from lxml import etree


# 根据微博名称查找博主信息
class Info:
    def __init__(self):
        logging.basicConfig(filemode='w',
                            filename='信息.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s : %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', )
        self.wb = openpyxl.Workbook()
        ws = self.wb['Sheet']
        self.wb.remove(ws)
        self.ws = self.wb.create_sheet('微博')
        self.ws.append(['昵称', '性别', 'ip属地', '出生日期', '粉丝数', '关注数', '公司', '学校', '信用', '描述', '个人签名', '创建时间', 'uid'])

    def __del__(self):
        self.wb.save('微博.xlsx')

    # 搜索框搜索用户,并找出用户uid和粉丝数和关注数
    def serach(self, name):
        url = 'https://weibo.com/ajax/side/search'
        params = {
            'q': name
        }
        n = 0
        while True:
            res = requests.get(url=url, params=params, headers=headers)
            if res.status_code == 200:
                user_list = res.json()['data']['users']
                for user in user_list:
                    if user['screen_name'] == name:
                        uid = user['id']
                        followers_count = user['followers_count']  # 粉丝数
                        friends_count = user['friends_count']  # 关注数
                        return [uid, followers_count, friends_count]
                else:
                    return None
            elif n < 5:
                n += 1
                print(f'请求  {name}  失败第{n}次,等待若干秒后继续请求')
                time.sleep(random.uniform(3, 6))
            else:
                return None

    # 搜索html查看是否存在
    def serach_html(self, name):
        url = 'https://s.weibo.com/weibo'
        params = {
            'q': name
        }
        res = requests.get(url=url, params=params, headers=headers)
        n = 0
        while True:
            if res.status_code == 200:
                try:
                    html = etree.HTML(res.text)
                    a = html.xpath('//div[@class="m-wrap"]/div[1]/div[1]/div[1]//div[@class="info"]/div/a[1]')[
                        0]  # 获取搜索昵称的a标签
                    h_name = a.xpath('./text()')[0]
                    if h_name == name:
                        href = a.xpath('./@href')[0]
                        uid = href.split('/')[-1]
                        uurl = 'https://weibo.com/ajax/profile/info'
                        res = requests.get(url=uurl + f'?custom={uid}', headers=headers).json()
                        followers_count = res['data']['user']['followers_count']  # 获取粉丝数
                        friends_count = res['data']['user']['friends_count']  # 获取关注数
                        return [uid, followers_count, friends_count]
                except IndexError:
                    n += 1
                    time.sleep(3)
            elif n < 5:
                n += 1
                print(f'请求  {name}  失败第{n}次,等待若干秒后继续请求')
                time.sleep(random.uniform(3, 6))
            else:
                return None

    # 请求用户的相关信息
    def request(self, uid, followers_count, friends_count, name):
        url = 'https://weibo.com/ajax/profile/detail'
        n = 0
        params = {
            'uid': uid
        }
        while True:
            res = requests.get(url=url, params=params, headers=headers)
            if res.status_code == 200:
                data = res.json()['data']
                created_at = data['created_at']  # 创建时间
                gender = data['gender']  # 性别
                if gender == 'f':
                    gender = '女'
                else:
                    gender = '男'
                description = data['description']  # 个人签名
                desc_text = data['desc_text']  # 描述
                try:
                    birthday = data['birthday']  # 出生日期
                except KeyError:
                    birthday = ''
                try:
                    ip_location = data['ip_location'].split('：')[-1]  # ip属地
                except KeyError:
                    ip_location = data['location']
                try:
                    company = data['company']  # 公司
                except KeyError:
                    company = ''
                try:
                    school = data['education']['school']  # 学校
                except KeyError:
                    school = ''
                level = data['sunshine_credit']['level']  # 信用
                self.save(
                    [name, gender, ip_location, birthday, followers_count, friends_count, company, school, level,
                     desc_text,
                     description,
                     created_at, uid])
                break
            elif n < 5:
                n += 1
                print(f'请求  {name}  详细信息失败第{n}次,等待若干秒后继续请求')
            else:
                logging.warning(f'---{name}---请求失败')
                break

    def save(self, data):
        self.ws.append(data)

    def run(self, data):
        for name in data:
            u = self.serach(name)
            if u:
                self.request(u[0], u[1], u[2], name)
                print(f'---{name}---抓取完毕')
                continue
            else:
                u = self.serach_html(name)
                if u:
                    self.request(u[0], u[1], u[2], name)
                    print(f'---{name}---抓取完毕')
                    continue
                else:
                    logging.info(f'---{name}---不存在')


if __name__ == '__main__':
    Info().run(['蹿紫', '鲜芋椰椰冰', '清新bot', 'SeanJohn-', '中国新闻周刊'])
