import scrapy
import time
import requests
from scrapy import cmdline
import sys, os
from urllib.parse import urlencode

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))
from items import WphItem


class GoodsSpider(scrapy.Spider):
    name = 'goods'
    # allowed_domains = ['xxx.com']
    start_urls = ['https://mapi.vip.com/vips-mobile/rest/shopping/pc/search/brand_store/get/v3']

    def __init__(self):
        super().__init__(GoodsSpider)
        self.goods_id_url = 'https://mapi.vip.com/vips-mobile/rest/shopping/pc/search/product/rank'
        self.datas_url = 'https://mapi.vip.com/vips-mobile/rest/shopping/pc/product/module/list/v2'

    @classmethod
    def get_mars_cid(cls):
        try:
            mars_cid = requests.get(url='http://127.0.0.1:5555/mars_cid').text
            return mars_cid
        except requests.exceptions.ConnectionError as f:
            raise ValueError('请先运行接口 js_port.js 文件')

    # goods
    def get_params(self, produces):
        params = {
            "app_name": "shop_pc",
            "app_version": "4.0",
            "warehouse": "VIP_NH",
            "fdc_area_id": "104104101",
            "client": "pc",
            "mobile_platform": "1",
            "province_id": "104104",
            "api_key": "70f71280d5d547b2a7bb370a529aeea1",
            "user_id": "",
            "mars_cid": GoodsSpider.get_mars_cid(),
            "wap_consumer": "a",
            "productIds": produces,
            "scene": "search",
            "standby_id": "nature",
            "extParams": "{\"stdSizeVids\":\"\",\"preheatTipsVer\":\"3\",\"couponVer\":\"v2\",\"exclusivePrice\":\"1\",\"iconSpec\":\"2x\",\"ic2label\":1,\"superHot\":1,\"bigBrand\":\"1\"}",
            "context": "",
            "_": f"{int(time.time() * 1000)}"
        }
        return params

    # goods
    def produce(self, produce_list, keyword):
        produces = ''
        for index, value in enumerate(produce_list):
            pid = value['pid']
            produces += str(pid) + ','
            if (index + 1) % 50 == 0:
                params = self.get_params(produces)
                url = self.datas_url + '?' + urlencode(params)
                yield scrapy.Request(url=url, callback=self.parse, meta={'type': keyword, })
                produces = ''
        if produces != '':
            params = self.get_params(produces)
            url = self.datas_url + '?' + urlencode(params)
            yield scrapy.Request(url=url, callback=self.parse, meta={'type': keyword, })

    def start_requests(self):
        mars_cid = GoodsSpider.get_mars_cid()
        type_list = ['口红']
        url = 'https://mapi.vip.com/vips-mobile/rest/shopping/pc/search/brand_store/get/v3'
        for t in type_list:
            params = {
                "app_name": "shop_pc",
                "app_version": "4.0",
                "warehouse": "VIP_NH",
                "fdc_area_id": "104104101",
                "client": "pc",
                "mobile_platform": "1",
                "province_id": "104104",
                "api_key": "70f71280d5d547b2a7bb370a529aeea1",
                "user_id": "",
                "mars_cid": mars_cid,
                "wap_consumer": "a",
                "keyword": f"{t}",
                "_": f"{int(time.time() * 1000)}"
            }
            data = urlencode(params)
            url = url + '?' + data
            yield scrapy.Request(url=url, callback=self.get_brand_id, meta={'type': t})

    def get_brand_id(self, response):
        keyword = response.meta['type']
        res = response.json()
        brand_list = res['data']['list']
        for value in brand_list:
            id = value['id']
            params = {
                "app_name": "shop_pc",
                "app_version": "4.0",
                "warehouse": "VIP_NH",
                "fdc_area_id": "104104101",
                "client": "pc",
                "mobile_platform": "1",
                "province_id": "104104",
                "api_key": "70f71280d5d547b2a7bb370a529aeea1",
                "user_id": "",
                "mars_cid": f"{GoodsSpider.get_mars_cid()}",
                "wap_consumer": "a",
                "standby_id": "nature",
                "keyword": f"{keyword}",
                "lv3CatIds": "",
                "lv2CatIds": "",
                "lv1CatIds": "",
                "brandStoreSns": f"{id}",
                "props": "",
                "priceMin": "",
                "priceMax": "",
                "vipService": "",
                "sort": "0",
                "pageOffset": "0",
                "channelId": "1",
                "gPlatform": "PC",
                "batchSize": "120",
                "_": f"{int(time.time() * 1000)}"
            }
            url = self.goods_id_url + '?' + urlencode(params)
            yield scrapy.Request(url=url, callback=self.get_goods,
                                 meta={'type': keyword, 'params': params})

    def get_goods(self, response):
        keyword = response.meta['type']
        res = response.json()
        # 判断该品牌是否存在商品
        try:
            produce_list = res['data']['products']
        except KeyError:
            pass
        else:
            is_last = res['data']['isLast']  # 是否为最后一页
            produces = ''
            if len(produce_list) > 50:
                if int(is_last) == 1:
                    self.produce(produce_list, keyword)
                else:
                    self.produce(produce_list, keyword)
                    goods_params = response.meta['params']
                    page_offset = int(goods_params['pageOffset']) + 120
                    goods_params['pageOffset'] = page_offset
                    url = self.goods_id_url + '?' + urlencode(goods_params)
                    yield scrapy.Request(url=url, callback=self.get_goods,
                                         meta={'type': keyword, 'params': goods_params})
            else:
                for index, value in enumerate(produce_list):
                    pid = value['pid']
                    produces += str(pid) + ','
                params = self.get_params(produces)
                url = self.datas_url + '?' + urlencode(params)
                yield scrapy.Request(url=url, callback=self.parse, meta={'type': keyword, })

    def parse(self, response):
        res = response.json()
        products_list = res['data']['products']
        for i in products_list:
            item = WphItem()
            item['brandShowName'] = i['brandShowName']
            item['title'] = i['title']
            try:
                item['marketPrice'] = i['price']['marketPrice']
            except KeyError as k:
                item['marketPrice'] = ''
            try:
                item['saleDiscount'] = i['price']['saleDiscount']
            except KeyError as k:
                item['saleDiscount'] = ''
            item['salePrice'] = i['price']['salePrice']
            yield item


if __name__ == '__main__':
    cmdline.execute('scrapy crawl goods'.split())
