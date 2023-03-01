import requests, sys, re, json, copy, os, logging, time
import redis, pymongo
from concurrent import futures
sys.path.append(sys.path[0])
from ytb_params import headers, jsons


class DB():
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client.ytb
        self.comment = self.db.comment

    def save(self, datas):
        self.comment.insert_many(datas)

    def save_one(self, data):
        self.comment.insert_one(data)


class YTB:
    def __init__(self, save_path=0):
        """
        :param save_path: 保存方式 默认为0本地文件,1为mongodb数据库,2为两者都保存
        """
        # 保存本地文件夹
        self.save_path = save_path
        if save_path == 0 or save_path == 2:
            if not os.path.exists(sys.path[0] + r'\视频评论'):
                os.mkdir(sys.path[0] + r'\视频评论')
            if save_path == 2:
                self.db = DB()
        elif save_path == 1:
            self.db = DB()
        else:
            raise ValueError('请选择其中一种方式存储')
        self.search_url = 'https://www.youtube.com/results'
        self.list_url = 'https://www.youtube.com/youtubei/v1/search?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false'
        self.comment_url = 'https://www.youtube.com/youtubei/v1/next?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false'
        self.noice = 0  # 统计次数
        self.redis_sql = redis.Redis(host='localhost', port=6379, db=0)
        self.redis_sql_1 = redis.Redis(host='localhost', port=6379, db=1)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            filename='log.log', filemode='a')

    def __del__(self):
        pass

    # 搜索出来的每一个视频页面数据
    def get_data(self, data, first=False):
        """
        :param data: 请求搜索框返回的 json数据
        :param first: 标记是否为第一次,False表示不是
        :return: 视频列表信息 [{},{}......] 形式
        """
        if first:
            lists = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer'][
                'contents']
            for i in lists:
                if list(i.keys())[0] == 'itemSectionRenderer':
                    contents_list = i['itemSectionRenderer']['contents']
                    d_list = []
                    for s in contents_list:
                        if list(s.keys())[0] == 'videoRenderer':
                            videoId = s['videoRenderer']['videoId']
                            title = s['videoRenderer']['title']['runs'][0]['text']
                            author = s['videoRenderer']['ownerText']['runs'][0]['text']
                            viewCount = s['videoRenderer']['viewCountText']['simpleText']
                            length = s['videoRenderer']['lengthText']['simpleText']
                            publishedTime = s['videoRenderer']['publishedTimeText']['simpleText']
                            d_list.append({
                                'videoId': videoId,
                                'title': title,
                                'author': author,
                                'viewCount': viewCount,
                                'length': length,
                                'publishedTime': publishedTime,
                            })
                    return d_list
                else:
                    pass
        else:
            c_list = data['onResponseReceivedCommands'][0]['appendContinuationItemsAction']['continuationItems']
            for c in c_list:
                if 'itemSectionRenderer' in list(c.keys()):
                    video_list = c['itemSectionRenderer']['contents']
                    d_list = []
                    for v in video_list:
                        if 'videoRenderer' in list(v.keys()):
                            videoId = v['videoRenderer']['videoId']
                            title = v['videoRenderer']['title']['runs'][0]['text']
                            author = v['videoRenderer']['ownerText']['runs'][0]['text']
                            viewCount = v['videoRenderer']['viewCountText']['simpleText']
                            length = v['videoRenderer']['lengthText']['simpleText']
                            publishedTime = v['videoRenderer']['publishedTimeText']['simpleText']
                            d_list.append({
                                'videoId': videoId,
                                'title': title,
                                'author': author,
                                'viewCount': viewCount,
                                'length': length,
                                'publishedTime': publishedTime,
                            })
                    return d_list

    # 连接代理
    def link_proxies(self):
        proxies = {'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'}
        return proxies

    # 请求搜索框
    def request(self, search, first=False, continuation=''):
        """
        :param search: 搜索内容
        :param first: 是否为第一次搜索(第一次搜索不存在continuation参数)
        :param continuation: 出去第一次每一次都需要携带的参数，支农从上一挑中获取
        :return: 网页script中的 js 数据和 token
        """
        if first:
            first_jsons = {
                'search_query': search
            }
            first_headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            }
            res = requests.get(url=self.search_url, headers=first_headers, params=first_jsons,
                               proxies=self.link_proxies())
            res_text = re.findall('var ytInitialData = (.*?)</script>', res.text)[0]
            res_text = res_text[:-1]
            res_json = json.loads(res_text)
            # 获取下次刷新需要的 continuation 参数
            contents = res_json['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer'][
                'contents']
            for c in contents:
                if 'continuationItemRenderer' in list(c.keys()):
                    token = c['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
            return res_json, token
        elif 'continuation' in list(jsons.keys()):
            jsons['continuation'] = continuation
            res = requests.post(url=self.list_url, headers=headers, json=jsons, proxies=self.link_proxies())
            # 获取下次刷新需要的 continuation 参数
            o_list = res.json()['onResponseReceivedCommands']
            for o in o_list:
                if 'appendContinuationItemsAction' in list(o.keys()):
                    t_list = o['appendContinuationItemsAction']['continuationItems']
                for t in t_list:
                    if 'continuationItemRenderer' in list(t.keys()):
                        token = t['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
                return res.json(), token
        else:
            print('参数错误')

    # 请求下载
    def down_request(self, url, method, videoId=0, token='', timeout=5):
        """
        :param url: 请求地址
        :param method: 请求方法
        :param videoId: 视频id号,为0抛出异常(不能为0)
        :param token: 评论需要的token参数
        :param timeout: 请求超时时间，默认5秒
        :return: res 响应
        """
        errorNoice = 0
        while True:
            try:
                if method == 'get':
                    if videoId == 0:
                        raise ValueError('视频id不能为0,videoId = ', videoId)
                    else:
                        params = {'v': videoId}
                    res = requests.get(url=url, params=params, headers=headers, proxies=self.link_proxies(),
                                       timeout=timeout)
                    return res
                elif method == 'post':
                    _jsons = copy.deepcopy(jsons)
                    _jsons['continuation'] = token
                    res = requests.post(url=url, json=_jsons, headers=headers, proxies=self.link_proxies(),
                                        timeout=timeout)
                    del _jsons
                    return res
                else:
                    raise ValueError('请求方法错误,', method)
            except requests.exceptions.Timeout as t:
                if errorNoice < 5:
                    time.sleep(10)
                    errorNoice += 1
                    logging.warning(f'请求超时第{errorNoice}次,等待十秒重连')
                else:
                    logging.warning(f'下载失败,请根据 uni')
                    raise requests.exceptions.ProxyError('下载失败')
            except requests.exceptions.ProxyError as r:
                if errorNoice < 5:
                    time.sleep(10)
                    errorNoice += 1
                    logging.warning(f'代理连接失败第{errorNoice}次,等待十秒重连')
                else:
                    raise requests.exceptions.ProxyError('代理失败')

    # 下载某一个视频下的评论信息
    def down_comment(self, videoId='', videoName='', video=''):
        """
        :param video: 视频数据,多线程并发使用
        :param videoId: 单独下载时的视频id
        :param videoName: 单独下载时的视频名字
        :return: None(进入解析函数)
        """
        if video != '':
            videoId = video['videoId']
            videoName = video['title']
        print(f'{videoId}------------------{videoName}')
        url = 'https://www.youtube.com/watch'
        res = self.down_request(url, 'get', videoId)
        self.noice += 1
        if res.status_code == 200:
            all_comment_list = []  # 总评论列表
            _list = 0  # 判断是否存在评论,0 为空
            _token = {}  # 用于判断是否存在下一页,不存在为{}
            flag = True  # 表示是否存在下一页
            html = res.text
            js_text = re.findall('var ytInitialData = (.*?);</script>', html)[0]
            js_json = json.loads(js_text)
            contents_list = js_json['contents']['twoColumnWatchNextResults']['results']['results']['contents']
            # 获取 token
            for c in contents_list:
                if 'itemSectionRenderer' in list(c.keys()):
                    if 'targetId' in list(c['itemSectionRenderer'].keys()):
                        # \ 换行
                        token = \
                            c['itemSectionRenderer']['contents'][0]['continuationItemRenderer']['continuationEndpoint'][
                                'continuationCommand']['token']
                        resComment = self.down_request(self.comment_url, 'post', 0, token)
                        resComment = resComment.json()
                        # 如果是最后一页 不存在_token参数,不是最后一页数据列表中的最后一条为有效数据
                        try:
                            # 判断是否还存在多页评论
                            _token = resComment['onResponseReceivedEndpoints'][1]['reloadContinuationItemsCommand'][
                                'continuationItems'][-1]['continuationItemRenderer']['continuationEndpoint'][
                                'continuationCommand']['token']
                        except KeyError as K:
                            flag = False
                        _list = self.isNull(resComment, flag)
                        if _list == 0:
                            pass
                        else:
                            all_comment_list.append(_list)
                        if flag:
                            pass
                        else:
                            self.save(all_comment_list, videoName)
                            if video != '':
                                self.drop_video_id(json.dumps(video), 'url')
                    else:
                        _list = 0
                else:
                    _list = 0
            # 判断是否还存在多页评论
            while True:
                if _list == 0 or _token == {}:
                    break
                _resComment = self.down_request(self.comment_url, 'post', 0, _token)
                _resComment = _resComment.json()
                self.noice += 1
                continuationItems = \
                    _resComment['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction'][
                        'continuationItems']
                try:
                    _token = continuationItems[-1]['continuationItemRenderer']['continuationEndpoint'][
                        'continuationCommand']['token']
                except KeyError as K:
                    flag = False
                _list = self.analysisComment(continuationItems, flag)
                all_comment_list.append(_list)
                if flag:
                    pass
                else:
                    self.save(all_comment_list, videoName)
                    if video != '':
                        self.drop_video_id(json.dumps(video), 'url')
                    break
        else:
            print(res.status_code)
            logging.warning(f'请求失败 ----{videoId}------------------{videoName}')
            pass

    # 判断评论是否为空
    def isNull(self, data_json, flag):
        """
        :param data_json: 评论的json数据
        :param flag: 判断是否存在下一页的表示
        :return: 为 0 则没有评论,否则进入解析函数
        """
        try:
            continuationItems = data_json['onResponseReceivedEndpoints'][1]['reloadContinuationItemsCommand'][
                'continuationItems']
            return self.analysisComment(continuationItems, flag)
        except KeyError as K:
            return 0

    # 区别是否是最后一页,非最后一页列表的最后一条数据不是评论数据
    def Flag(self, continuationItems, flag):
        if flag:
            return continuationItems[:-1]
        else:
            return continuationItems

    # 解析评论
    def analysisComment(self, continuationItems, flag):
        """
        :param continuationItems: 评论列表
        :param flag: 下一页旗帜
        :return: 该页的所有评论 list
        """
        comment_list = []
        for c in self.Flag(continuationItems, flag):
            commentRenderer = c['commentThreadRenderer']['comment']['commentRenderer']
            text_list = commentRenderer['contentText']['runs']
            _comment = ''
            for t in text_list:
                _comment += t['text']
            author = commentRenderer['authorThumbnail']['accessibility']['accessibilityData']['label']
            try:
                authorId = commentRenderer['authorEndpoint']['browseEndpoint']['browseId']
            except KeyError as k:
                author = '__该用户名为空__'
            publishedTime = commentRenderer['publishedTimeText']['runs'][0]['text']
            # 点赞 存在 o 点赞的可能
            try:
                voteCount = commentRenderer['voteCount']['simpleText']
            except KeyError as K:
                voteCount = '0'
            dict_obj = {'comment': _comment, 'author': author, 'authorId': authorId, 'publishedTime': publishedTime,
                        'voteCount': voteCount}
            comment_list.append(dict_obj)
        return comment_list

    # 使用正则表达式替换 Windows 系统不允许的字符
    def normalize_filename(self, filename):
        pattern = r'[<>:"/\\|?*]'
        return re.sub(pattern, '_', filename)

    # 保存评论数据
    def save(self, dict_obj, videoName):
        """
        :param dict_obj: 数据列表
        :param videoName: 文件名
        :return:
        """
        if self.save_path == 2:
            self.local(dict_obj, videoName)
            self.save_sql(dict_obj)
        elif self.save_path == 0:
            self.local(dict_obj, videoName)
        elif self.save_path == 1:
            self.save_sql(dict_obj)

    # 保存在本地文件夹
    def local(self, dict_obj, videoName):
        """
        :param dict_obj: 数据
        :param videoName: 文件名
        :return:
        """
        videoName = self.normalize_filename(videoName)
        with open(sys.path[0] + f'\视频评论\{videoName}.json', 'a', encoding='utf-8') as f:
            json.dump(dict_obj, f, ensure_ascii=False)

    # 保存进 mongodb 数据库
    def save_sql(self, data):
        """
        :param data: 数据 list[list]
        :return:
        """
        for d in data:
            self.db.save(d)

    # url 去重
    def unique_url(self, lists, collect):
        """
        :param collect: 集合
        :param lists: video_id 列表
        :return: None
        """
        for l in lists:
            json_str = json.dumps(l)
            self.redis_sql.sadd(collect, json_str)

    # 断点续爬
    def continue_spider(self, num):
        """
        :param num: 线程数
        :return:
        """
        # 判断是否为空
        if self.redis_sql.scard('url') != 0:
            logging.info('开启断点续爬')
            self.thread_collection(num)

    # 随机获取一个video_id
    def get_video_id(self, collect):
        """
        :param collect: 集合
        :return:
        """
        video_id = self.redis_sql.srandmember(collect)
        video_id = json.loads(video_id)
        return video_id

    # 请求完毕后删除video_id
    def drop_video_id(self, video, collect):
        """
        :param video: 初始整个的video信息
        :param collect: 集合
        :return:
        """
        self.redis_sql.srem(collect, video)

    # 线程池
    def thread_collection(self, num, collect):
        """
        :param num: 并发数
        :return:
        """
        with futures.ThreadPoolExecutor(max_workers=num) as executor:
            tasks = []
            while True:
                # 判断是否为空
                if self.redis_sql.scard(collect) != 0:
                    video_id = self.get_video_id(collect)
                    tasks.append(executor.submit(self.down_comment, video=video_id))
                    self.redis_sql.sadd('url', json.dumps(video_id))
                    self.drop_video_id(json.dumps(video_id), collect)
                else:
                    break
            logging.info('任务全部添加进列表，开始爬虫')
            results = []
            for task in futures.as_completed(tasks):
                result = task.result()
                results.append(result)

    def runs(self, search, page=1, num=5):
        """
        :param search: 搜索内容
        :param page: 页数
        :param num: 线程数
        :return:
        """
        collect = 'unique_url'
        logging.info('开始爬虫')
        _t = time.time()
        data_json, token = self.request(search, first=True)
        lists = self.get_data(data_json, first=True)
        self.unique_url(lists, 'unique_url')
        if page > 1:
            for i in range(1, page):
                data_json, token = self.request(search='', continuation=token)
                lists = self.get_data(data_json)
                self.unique_url(lists, 'unique_url')
        logging.info('所有任务已经存进redis，下面开始多线程采集')
        self.thread_collection(num, collect)
        _tt = time.time() - _t
        print(_tt)
        print(self.noice)
        logging.info(f'爬虫结束，耗时{_tt}，共发{self.noice}次请求')


if __name__ == '__main__':
    YTB(2).runs('美国', page=1, num=5)
