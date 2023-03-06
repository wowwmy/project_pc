import requests
import execjs
from lxml import etree
import os, sys, time
import threading
from queue import Queue
sys.path.insert(0, os.path.abspath(os.path.join('.')))
from sql import link, close_link, insert_data


class THS:
    def __init__(self):
        self.url = 'http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/{}/ajax/1/'
        with open('v.js', 'r', encoding='utf-8') as f:
            js_txt = f.read()
        self.js_compile = execjs.compile(js_txt)
        self.session = link()
        self.data_queue = Queue()

    def get_v(self):
        return self.js_compile.call('get_v')

    def request(self, page):
        v = self.get_v()
        headers = {
            "Cookie": 'v='.join(v),
            "hexin-v": v,
            "Host": "q.10jqka.com.cn",
            "Referer": "http://q.10jqka.com.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        }
        url = self.url.format(page)
        res = requests.get(url=url, headers=headers)
        self.parse(res)

    def parse(self, res):
        res = res.text
        html = etree.HTML(res)
        tbody = html.xpath('//tbody/tr')
        for tr in tbody:
            order_number = tr.xpath('./td[1]/text()')[0]
            stock_code = tr.xpath('./td[2]/a/text()')[0]
            stock_name = tr.xpath('./td[3]/a/text()')[0]
            current_price = tr.xpath('./td[4]/text()')[0]
            up_down_range = tr.xpath('./td[5]/text()')[0]
            up_down = tr.xpath('./td[6]/text()')[0]
            increase_speed = tr.xpath('./td[7]/text()')[0]
            change_hands = tr.xpath('./td[8]/text()')[0]
            maximum_ratio = tr.xpath('./td[9]/text()')[0]
            amplitude = tr.xpath('./td[10]/text()')[0]
            turnover = tr.xpath('./td[11]/text()')[0]
            tradable_stock = tr.xpath('./td[12]/text()')[0]
            market_value = tr.xpath('./td[13]/text()')[0]
            p_e_ratio = tr.xpath('./td[14]/text()')[0]
            self.save_queue(
                [order_number, stock_code, stock_name, current_price, up_down_range, up_down, increase_speed,
                 change_hands, maximum_ratio, amplitude, turnover, tradable_stock, market_value, p_e_ratio])


    def save_queue(self, data):
        for index, value in enumerate(data):
            if value == '--':
                data[index] = 0.0
            elif index in [3, 4, 5, 6, 7, 8, 9]:
                data[index] = float(data[index])
            else:
                pass
        self.data_queue.put([int(data[0]), int(data[1]), data[2], data[3], data[4], data[5],
                             data[6], data[7], data[8], data[9], data[10], data[11], data[12],
                             data[12]])

    def save(self):
        n = 0
        while n < 10:
            if self.data_queue.empty():
                n += 1
                time.sleep(0.5)
            else:
                n = 0
                data = self.data_queue.get()
                insert_data(self.session, data[0], data[1], data[2], data[3], data[4], data[5],
                            data[6], data[7], data[8], data[9], data[10], data[11], data[12],
                            data[12])

    def run(self, page):
        start_t = time.time()
        threads = []
        if isinstance(page, int) and page > 0:
            for p in range(1, page + 1):
                threads.append(
                    threading.Thread(target=self.request, args=(p,))
                )
            queue = threading.Thread(target=self.save, )
            queue.start()
            for thread in threads:
                thread.start()
            queue.join()
            for thread in threads:
                thread.join()
        else:
            raise ValueError('请输入整数')
        close_link(self.session)
        print('耗时:', time.time() - start_t)


if __name__ == '__main__':
    THS().run(246)
