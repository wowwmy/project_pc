import requests
from lxml import etree
import threading
import logging
import time, random
import openpyxl
from tqdm import tqdm


class Disease:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        # 统计需要请求次数
        self.number = 0
        # 统计总请求次数
        self.numbers = 0
        logging.basicConfig(
            filename='log.log',
            filemode='w',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s : %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )

    def request(self, url):
        """
        请求
        :param url: 请求地址
        :return: 响应 或 None
        """
        n = 0
        c = 0
        self.number += 1
        while True:
            self.numbers += 1
            try:
                res = requests.get(url=url, headers=self.headers)
                if res.status_code == 200:
                    return res
                elif n < 5:
                    n += 1
                    logging.info(f'网页{url},请求状态失败{n}次，状态码 {res.status_code}')
                    print(f'网页{url},请求状态失败{n}次，状态码 {res.status_code}')
                    time.sleep(random.uniform(1, 2))
                else:
                    logging.info(f'网页{url},请求失败,请手动查询原因')
                    return None
            except requests.exceptions.ConnectionError:
                time.sleep(random.uniform(2, 5))
                c += 1
                if c > 5:
                    logging.error(f'网页{url},请求失败{c}次,停止访问')
                    return None

    def home_page(self):
        """
        获取所有科室
        :return: 科室列表
        """
        url = 'https://jbk.39.net/bw/'
        res = self.request(url=url)
        html = etree.HTML(res.text)
        # 科室列表
        uls = html.xpath('//div[@class="lookup_box"]/div[1]/div/ul')
        lis = []
        for ul in uls:
            li_s = ul.xpath('./li')
            for li in li_s:
                url = li.xpath('./a/@href')[0]
                name = li.xpath('./a/text()')[0]
                lis.append({'url': 'https://jbk.39.net' + url, 'name': name})
        # 切片去掉不限科室
        return lis[1:]

    def kind_page(self, data):
        """
        某一类下的所有页面请求
        :param data: 科室数据
        :return:
        """
        home_url = data['url']
        name = data['name']
        ws = self.wb.create_sheet(title=name)
        ws.append(['疾病', '症状'])
        # 分割出 种类
        kind = home_url.split('/')[-1].split('_')[0]
        res = self.request(url=home_url)
        html = etree.HTML(res.text)
        spans = html.xpath('//ul[@class="result_item_dots"]/li/span')
        # 总页数
        try:
            pages = spans[-2].xpath('./a/text()')[0]
            for page in tqdm(range(1, int(pages) + 1), desc=name, position=0,ncols=100,colour='blue'):
                url = f'https://jbk.39.net/bw/{kind}_t1_p{page}'
                self.details(url, ws)
        except IndexError:
            url = f'https://jbk.39.net/bw/{kind}_t1'
            self.details(url, ws)

    def details(self, url, ws):
        """
        详情页解析数据
        :param url: 地址
        :param ws: xlsx
        :return:
        """
        res = self.request(url=url)
        if res:
            html = etree.HTML(res.text)
            divs = html.xpath('//div[@class="result_content"]/div')
            for div in divs:
                try:
                    ill_name = div.xpath('./div/p[1]/a/text()')[0]
                    symptom = div.xpath('./p[2]/a//text()')
                    self.save(ill_name, symptom, ws)
                #  核医学科 不存在这个元素(没有疾病)
                except IndexError:
                    pass

    def convert(self, l):
        s = ''
        for i in l:
            s += i + ' '
        return s

    def save(self, ill_name, symptom, ws):
        """
        保存
        :param ill_name: 疾病名
        :param symptom: 症状
        :param ws: xlsx
        :return:
        """
        ws.append([ill_name, self.convert(symptom)])

    def kind(self, data):
        """
        科室下的种类
        :param data: 科室的数据
        :return: None
        """
        main_url = data['url']
        main_name = data['name']
        res = self.request(url=main_url)
        html = etree.HTML(res.text)
        lis = html.xpath('//div[@class="lookup_box"]/div[1]/div[2]/ul/li')
        if len(lis) == 0:
            self.kind_page({'url': main_url[:-1] + '_t1_p1', 'name': main_name})
        else:
            for li in lis:
                name = li.xpath('./a/text()')[0]
                url = li.xpath('./a/@href')[0]
                self.kind_page({'url': 'https://jbk.39.net' + url[:-1] + '_t1_p1', 'name': name})

    def run(self):
        logging.info('--------------开始爬虫------------')
        start_time = time.time()
        lis = self.home_page()
        threads = []
        for li in lis:
            thread = threading.Thread(target=self.kind, args=(li,))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        t = time.time() - start_time
        logging.info('--------------日志简报------------')
        logging.info(f'需要请求   : {self.number}')
        logging.info(f'总请求数   : {self.numbers}')
        logging.info(f'请求成功率 : {self.number / self.numbers}')
        logging.info(f'请求耗时   : {t}')
        logging.info(f'平均耗时   : {t / self.numbers}')
        logging.info(f'使用线程   : {len(threads)}')

    def __del__(self):
        self.wb.save('疾病.xlsx')


if __name__ == '__main__':
    Disease().run()
