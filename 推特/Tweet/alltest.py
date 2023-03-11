import httpx
import openpyxl
import datetime
import time
import re

wb = openpyxl.Workbook()
ws = wb.create_sheet(title='huawei', index=0)
ws.append(['推文', '发布时间', '阅读量', '点赞', '回复数', '转发数'])
# 统计数量
num = 0


def datetimes(start, end):
    '''
    :param start: 格式 2000-1-1,type:str
    :param end: 格式 2000-1-1,type:str
    :return: 2000-1-1
    '''
    start_date_list = start.split('-')
    start_year = int(start_date_list[0])
    start_month = int(start_date_list[1])
    start_day = int(start_date_list[2])
    end_date_list = end.split('-')
    end_year = int(end_date_list[0])
    end_month = int(end_date_list[1])
    end_day = int(end_date_list[2])
    # 遍历日期
    start_date = datetime.date(start_year, start_month, start_day)
    end_date = datetime.date(end_year, end_month, end_day)
    delta = datetime.timedelta(days=1)
    while start_date <= end_date:
        yield start_date.strftime('%Y-%m-%d')
        start_date += delta


def request(start_time, end_time, username):
    proxies = 'http://127.0.0.1:10809'
    url = 'https://api.twitter.com/2/search/adaptive.json'
    dates = datetimes(start_time, end_time)
    start = dates.__next__()
    for i in dates:
        c = 1
        print(start)
        params = {
            "include_profile_interstitial_type": 1,
            "include_blocking": 1,
            "include_blocked_by": 1,
            "include_followed_by": 1,
            "include_want_retweets": 1,
            "include_mute_edge": 1,
            "include_can_dm": 1,
            "include_can_media_tag": 1,
            "include_ext_has_nft_avatar": 1,
            "include_ext_is_blue_verified": 1,
            "include_ext_verified_type": 1,
            "skip_status": 1,
            "cards_platform": "Web-12",
            "include_cards": 1,
            "include_ext_alt_text": True,
            "include_ext_limited_action_results": False,
            "include_quote_count": True,
            "include_reply_count": "1",
            "tweet_mode": "extended",
            "include_ext_views": True,
            "include_entities": True,
            "include_user_entities": True,
            "include_ext_media_color": True,
            "include_ext_media_availability": True,
            "include_ext_sensitive_media_warning": True,
            "include_ext_trusted_friends_metadata": True,
            "send_error_codes": True,
            "simple_quoted_tweet": True,
            "q": f"from:{username} since:{start} until:{i}",
            "query_source": "typed_query",
            "count": '20',
            "requestContext": "launch",
            "pc": 1,
            "spelling_corrections": 1,
            "include_ext_edit_control": True,
            "ext": "mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,enrichments,superFollowMetadata,unmentionInfo,editControl,vibe"
        }
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "cache-control": "no-cache",
            "cookie": "guest_id_ads=v1%3A167843297909027004; guest_id_marketing=v1%3A167843297909027004; guest_id=v1%3A167843297909027004; external_referer=padhuUp37zhD6%2F29CpQtyhGQCUl05AFo|0|8e8t2xd8A2w%3D; lv-uid=AAAAEICJd1PxqMh97uVn--bxkHEGNmhfiPfZJf5PwNYvTcTqt9SIDnP-6_xnDKR6; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCE7RUcuGAToMY3NyZl9p%250AZCIlNDE5NzU3ODllNDBmYWRmZmEwNTEwMGZiMGM5OWUyMTY6B2lkIiUwNDZh%250ANzRlNjRhNTg1YTM2NTAwMzA4MGNlYzVlMjBhYg%253D%253D--0452bb956ad1fc25a53e90dd468de4ca3d341d0e; kdt=pPUoNjoMjggtBgauGBtRS1xUpxQkRfIymVcnOl3z; auth_token=712b02e4303f75db539bb7d5df3a6ad69b3c4269; ct0=17afbbaa2086c51b85e937c3f453bc6ebcccaf3bab9be9fda46d1865afc4168b43dfe21dccbee6c66e09516d12f7f80b6ff04775c78a50d575d7fb3d6d7d121de0a7cac890969cb2145c84795b4c6d42; att=1-3wH2vAgjX6tYPr4V5rBrc22RK2YHyReCmjqWfgaT; twid=u%3D1595489338401251329; personalization_id=\"v1_ZEbdWA7oI5oxtmJtpIHNIA==\"",
            "origin": "https://twitter.com",
            "pragma": "no-cache",
            "referer": "https://twitter.com/",
            "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "x-csrf-token": "17afbbaa2086c51b85e937c3f453bc6ebcccaf3bab9be9fda46d1865afc4168b43dfe21dccbee6c66e09516d12f7f80b6ff04775c78a50d575d7fb3d6d7d121de0a7cac890969cb2145c84795b4c6d42",
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "en"
        }
        code = []
        while True:
            try:
                n = 1
                res = httpx.get(url=url, params=params, headers=headers, proxies=proxies, timeout=20)
                c += 1
                if res.status_code == 200:
                    parse(res.json(), start)
                    start = i
                    break
                elif c > 5:
                    raise ValueError('响应超过5次非正常状态码', code)
                else:
                    time.sleep(5)
                    code.append(res.status_code)
            except httpx._exceptions.ProxyError:
                if n > 5:
                    raise httpx._exceptions.ProxyError('代理重连失败超过五次,检查代理是否可以上网')
                else:
                    time.sleep(10)
                    n += 1
            except httpx.ConnectTimeout:
                if n > 5:
                    raise httpx.ConnectTimeout('代理重连失败超过五次,检查代理是否可以上网')
                else:
                    time.sleep(10)
                    print('连接超时，等待十秒')
                    n += 1
            except httpx.ConnectError:
                if n > 5:
                    raise httpx.ConnectError('代理重连失败超过五次,检查代理是否可以上网')
                else:
                    time.sleep(10)
                    print('连接超时，等待十秒')
                    n += 1


def parse(res, start):
    # 依然还是一个字典（推文id:{}形式），将里面的value提取出来
    try:
        tweets = res['globalObjects']['tweets']
    except KeyError:
        print(res)
    global num
    num += len(tweets)
    # 没有推文tweets为空{},不会报错
    for t in tweets:
        tweet = tweets[t]['full_text']
        published = start + ' ' + re.findall(r'\d{2}:\d{2}:\d{2}', tweets[t]['created_at'])[0]
        reply_count = tweets[t]['reply_count']
        retweet_count = int(tweets[t]['retweet_count']) + int(tweets[t]['quote_count'])
        favorite_count = tweets[t]['favorite_count']
        try:
            views = tweets[t]['ext_views']['count']
        except KeyError:
            views = ''
        print('tweet-->', tweet)
        print('published-->', published)
        save(tweet, published, reply_count, retweet_count, favorite_count, views)
    print('-' * 20, f'已采集{num}条', '-' * 20)


def save(tweet, published, reply_count, retweet_count, favorite_count, views):
    ws.append([tweet, published, views, favorite_count, reply_count, retweet_count])


def run():
    # 结束日期需要往后推一天
    # request('2009-12-1', '2023-3-12', 'huawei')
    request('2023-3-10', '2023-3-11', 'huawei')
    wb.save('Tweet_all.xlsx')


if __name__ == '__main__':
    run()
    # pass
