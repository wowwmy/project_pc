# @Time : 2022/10/08 14:58
# @Author : NDY
# @File : DZ.py
import time
import random
import requests
import re
from lxml import etree


class DZDP:
    def __init__(self, html_url):
        # 地址需要留意是否已经变化
        # self.svg_url = 'https://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/fc55477bfd00e8bfb8300ceb65768190.svg'
        # self.css_url = 'https://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/b76af2f09418ee5b33a42407f10876a5.css'
        self.html_url = html_url
        # 登录后的 headers
        self.headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "s_ViewType=10; _lxsdk_cuid=181e22c8eb8c8-086ec3bd373e0f-26021a51-144000-181e22c8eb8c8; _lxsdk=181e22c8eb8c8-086ec3bd373e0f-26021a51-144000-181e22c8eb8c8; _hc.v=c174b137-0274-9e22-5f2d-567672e7fdaf.1657356980; WEBDFPID=24x51x1x8w4x50y1z63x838164z152x5816y42zz18y979586y68v9y2-1980557057446-1665197057117KMKOAKQfd79fef3d01d5e9aadc18ccd4d0c95072876; ctu=d5d70d6840d6541e801ed6c702ec26c57559be5ad80a3f3dd12cff156245a945; cy=58; cye=anshan; ua=dpuser_6393149767; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666421660,1666425161,1666510090,1667564607; dplet=5a5948a71951b8f3909e754f15167b68; dper=4cbaf8aab2a1ecd097f277d5e7cc5f35f0657c2e7502c0f587d905d196582feea7fe5e2280c1b4fa0ca12730f0a6489587ea48e22162f2b998ca3bfa42ae4ee55d9ade0f322a5fefb2081ac5a80f2aaa0c31df19b0a878f2d776d2dfcb187960; ll=7fd06e815b796be3df069dec7836c3df; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1667569342; _lxsdk_s=18442dd35a9-c06-ee2-b91%7C%7C1484",
    "Host": "www.dianping.com",
    "Pragma": "no-cache",
    "Referer": "https://www.dianping.com/shop/EzgJJU7ShvUKQwiB/review_all/p261",
    "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

    def find_svg_css(self):
        res = requests.get(url=self.html_url, headers=self.headers).text
        css = re.findall('//s3plus.meituan.net/v1(.*?)">', res)[0]
        self.css_url = 'https://s3plus.meituan.net/v1' + css
        print(self.css_url)
        css_res = requests.get(url=self.css_url).text
        # 获取svg的三个类名
        svg = re.findall(r'class\^=(.*?)}', css_res)
        # 获取svg使用的类名
        svg_class_name = re.findall(r'<svgmtsi class="(.*?)"></svgmtsi>', res)[0]
        # 获取正确的svg文件名
        for s in svg:
            class_name = re.findall('"(.*?)"', s)
            if class_name[0] in svg_class_name:
                svg = re.findall(r'background-image: url\((.*?)\);', s)[0]
                self.svg_url = 'https:' + svg
                print(self.svg_url)
                break

    # 下载 svg 和 css 文件
    def get_svg_css(self):
        self.svg_text = requests.get(self.svg_url).text
        css_text = requests.get(self.css_url).text
        # 将换行符与空格清除，方便下一步匹配
        self.css_text = css_text.replace('\n', '').replace(' ', '')

    # 请求网页
    def request_url(self, url, page=1):
        if page > 2:
            pass
        else:
            self.headers['Referer'] = f'https://www.dianping.com/shop/EzgJJU7ShvUKQwiB/review_all/p{page - 1}'
        html_text = requests.get(url, headers=self.headers).text
        return html_text

    # 寻找出svg文件中定义的字符大小
    def find_font_size(self, in_text):
        fs = re.compile(r'font-size:(\d+)px')
        res = fs.findall(in_text)
        return int(res[0])

    # 返回字符所在行数
    # number 为 y 坐标
    def find_height_lines(self, number, svg_text):
        path = re.findall(r'<path(.*?)>', svg_text)
        if path == []:
            path = re.findall(r'<text(.*?)>', svg_text)
        for index, p in enumerate(path):
            try:
                d = re.findall('d="M0 (.*?) H', p)[0]
                id = re.findall('id="(.*?)"', p)[0]
                if number <= int(d):
                    return int(id)
            except IndexError:
                y = re.findall('y="(.*?)"', p)[0]
                if number <= int(y):
                    return int(index) + 1

    # 获取字体
    # 行数, x 坐标, 字体大小
    def get_font(self, line, x, font_size, svg_text):
        all_font = re.findall(r'<textPath(.*?)</textPath>', svg_text)
        if all_font == []:
            all_font = re.findall(r'<text(.*?)</text>', svg_text)
        for index, a in enumerate(all_font):
            font = re.findall('[\u4e00-\u9fa5]+', a)[0]
            if index + 1 == line:
                f = int(x / font_size)
                return font[f:f + 1]

    # 定义一个函数用于匹配class属性为xx对应的css参数(x和y值)
    def find_xy(self, in_text, class_value):
        re_sentence = r'.%s{background:-(.*?)px-(.*?)px;}' % class_value
        pattern = re.compile(re_sentence)
        res = pattern.findall(in_text)
        return res[0]

    # 替换被处理的字体
    def replace_html(self, html_text, css_text, svg_text):
        tq = re.findall('<svgmtsi class="(.*?)">', html_text)
        for t in tq:
            x, y = self.find_xy(css_text, t)
            font_size = self.find_font_size(svg_text)
            line = self.find_height_lines(int(float(y)), svg_text)
            font = self.get_font(line, int(float(x)), font_size, svg_text)
            # 处理字体
            html_text = re.sub('<svgmtsi class="' + t + '"></svgmtsi>', font, html_text)
        return html_text

    # 解析(数据所在，根据自身要求保存)
    def parse(self, html_text):
        HTML = etree.HTML(html_text)
        li_list = HTML.xpath('//div[@class="reviews-items"]/ul/li')
        for l in li_list:
            try:
                username = l.xpath('./div[@class="main-review"]/div[@class="dper-info"]/a/text()')[0]
                username = username.replace('\n', '').replace(' ', '')
                print(username)
            except IndexError:
                username = l.xpath('./div[@class="main-review"]/div[@class="dper-info"]/span[@class="name"]/text()')[0]
                username = username.replace('\n', '').replace(' ', '')
                print(username)
            # 评分 环境 等等
            flavor = l.xpath('./div[@class="main-review"]/div[@class="review-rank"]/span[@class="score"]/span')
            for f in flavor:
                i = f.xpath('./text()')[0]
                i = i.replace('\n', '').replace(' ', '')
                print(i)
            # 评论过短会不存在review-words Hide这个属性
            comment_ = ''
            comment = l.xpath('./div[@class="main-review"]/div[@class="review-words Hide"]/text()')
            for c in comment:
                comment_ += c
            comment_ = comment_.replace('\n', '').replace(' ', '').replace('\t', '')
            if comment_ == '':
                comment = l.xpath('./div[@class="main-review"]/div[@class="review-words"]/text()')[0]
                comment = comment.replace('\n', '').replace(' ', '').replace('\t', '')
                print(comment)
            else:
                print(comment_)
            # 发布时间
            pub_time = l.xpath('./div//span[@class="time"]/text()')[0]
            pub_time = pub_time.replace('\n', '').strip()
            print(pub_time)
            print('-' * 80)

    # 根据需要自己定制
    def save(self, ):
        pass

    def run(self, page=0, all_page=False):
        self.find_svg_css()
        self.get_svg_css()
        html_text = self.request_url(self.html_url)
        html_text = self.replace_html(html_text, self.css_text, self.svg_text)
        with open('1.html', 'w', encoding='utf-8') as f:
            f.write(html_text)
        self.parse(html_text)
        while all_page:
            time.sleep(random.uniform(2.5, 3))
            ht = etree.HTML(html_text)
            try:
                next_page = ht.xpath('//div[@class="reviews-pages"]/a[text()="下一页"]/@data-pg')[0]
            except IndexError:
                with open('222.html', 'w', encoding='utf-8') as f:
                    f.write(html_text)
                break
            html = f'{self.html_url}/p{next_page}'
            print(html)
            html_text = self.request_url(html, int(next_page))
            html_text = self.replace_html(html_text, self.css_text, self.svg_text)
            self.parse(html_text)

        if page >= 2 and all_page == False:
            for i in range(2, page + 1):
                time.sleep(random.uniform(2.5, 3))
                html = f'{self.html_url}/p{i}'
                print(html)
                html_text = self.request_url(html, i)
                html_text = self.replace_html(html_text, self.css_text, self.svg_text)
                self.parse(html_text)


if __name__ == '__main__':
    # 商家地址
    id = 'Fu9mQKxeMFu1EDi8'
    start_time = time.time()
    url = 'https://www.dianping.com/shop/' + id
    html_url = url + '/review_all'
    # 爬多少页 默认首页
    page = 1
    # all_page 为True 爬取全部评论 优先级比 page 高
    DZDP(html_url).run(page=page, all_page=True)
    print('消耗时间>>>', time.time() - start_time)
