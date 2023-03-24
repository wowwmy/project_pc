import requests
from head import headers
import time, random
import logging
import openpyxl


# 只抓取该博主自己的文章
class Text:
    def __init__(self):
        # logging.basicConfig(
        #     level=logging.DEBUG,
        #     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s-%(funcName)s',
        # )
        self.n = 0
        self.wb = openpyxl.Workbook()
        ws = self.wb['Sheet']
        self.wb.remove(ws)
        self.ws = self.wb.create_sheet('微博')
        self.ws.append(['作者', '创建时间', '发布地点', '点赞数', '回复数', '转发数', '文本'])

    def __del__(self):
        self.wb.save('微博.xlsx')

    def request(self, uid):
        url = 'https://weibo.com/ajax/statuses/mymblog'
        params = {
            "uid": f"{uid}",
            "page": "1",
            "feature": "0"
        }
        page = 1
        while True:
            n = 0
            while True:
                res = requests.get(url=url, params=params, headers=headers)
                if res.status_code == 200:
                    since_id = self.parse(res.json(), uid)
                    break
                elif n < 5:
                    n += 1
                    logging.warning('请求失败{n}次,等待若干秒后重新请求')
                    time.sleep(random.uniform(3, 6))
                else:
                    raise requests.ConnectionError(f'{res.json()}')
            if since_id:
                page += 1
                params = {
                    "uid": f"{uid}",
                    "page": f"{page}",
                    "feature": "0",
                    "since_id": since_id,
                }
            else:
                break

    # 获取文章的长(全部)文本
    def all_text(self, mblogid):
        url = 'https://weibo.com/ajax/statuses/longtext'
        res = requests.get(url=url + f'?id={mblogid}', headers=headers).json()
        if res['data'] == {}:
            return None
        text = res['data']['longTextContent']
        return text

    def parse(self, data, uid):
        lists = data['data']['list']
        for l in lists:
            user = l['user']['screen_name']  # 用户名
            uids = l['user']['id']
            mblogid = l['mblogid']
            text = self.all_text(mblogid)  # 文本
            if text:
                pass
            else:
                text = l['text_raw']
            creat_time = l['created_at']  # 创建时间
            try:
                region_name = l['region_name'][4:]  # 发布地点
            except KeyError:
                region_name = ''
            support = l['attitudes_count']  # 点赞
            reply_count = l['comments_count']  # 回复数
            repeat_count = l['reposts_count']  # 转发数
            self.n += 1
            print(f'-----------------------------{self.n}------------------------------')
            if uids == uid:
                self.save([user, creat_time, region_name, support, reply_count, repeat_count, text])
        since_id = data['data']['since_id']
        return since_id

    def save(self, data):
        self.ws.append(data)

    def run(self, uid):
        self.request(uid)


if __name__ == '__main__':
    Text().run(5996241771)
