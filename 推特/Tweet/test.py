import requests
import openpyxl
import time

proxies = {
    'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'
}

wb = openpyxl.Workbook()
ws = wb.create_sheet(title='华为', index=0)
ws.append(['推文', '发布时间', '阅读量', '点赞', '回复数', '转发数', '是否属于转发'])
order = 0
num = 0
# 获取 guest_token 值
def token():
    url = 'https://api.twitter.com/1.1/guest/activate.json'
    headers = {
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    }
    res = requests.post(url=url, proxies=proxies, headers=headers).json()
    return res['guest_token']


def request(userid, cursor='', ):
    url = 'https://api.twitter.com/graphql/juVPUUIyd5BdOivC5ROVHQ/UserTweets'
    params = {
        'variables': {"userId": userid, "count": 40, "includePromotedContent": True,
                      "withQuickPromoteEligibilityTweetFields": True,
                      "withSuperFollowsUserFields": True,
                      "withDownvotePerspective": False, "withReactionsMetadata": False,
                      "withReactionsPerspective": False, "withSuperFollowsTweetFields": True,
                      "withVoice": True,
                      "withV2Timeline": True},
        'features': {"responsive_web_twitter_blue_verified_badge_is_enabled": True,
                     "responsive_web_graphql_exclude_directive_enabled": True,
                     "verified_phone_label_enabled": False,
                     "responsive_web_graphql_timeline_navigation_enabled": True,
                     "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                     "tweetypie_unmention_optimization_enabled": True, "vibe_api_enabled": True,
                     "responsive_web_edit_tweet_api_enabled": True,
                     "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                     "view_counts_everywhere_api_enabled": True,
                     "longform_notetweets_consumption_enabled": True, "tweet_awards_web_tipping_enabled": False,
                     "freedom_of_speech_not_reach_fetch_enabled": False, "standardized_nudges_misinfo": True,
                     "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
                     "interactive_text_enabled": True, "responsive_web_text_conversations_enabled": False,
                     "longform_notetweets_richtext_consumption_enabled": False,
                     "responsive_web_enhance_cards_enabled": False}
    }
    if cursor == '':
        pass
    else:
        params['variables']['cursor'] = cursor
    headers = {
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "content-type": "application/json",
        "origin": "https://twitter.com",
        "referer": "https://twitter.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "x-guest-token": token(),
        "x-twitter-active-user": "no",
        "x-twitter-client-language": "zh-cn"
    }
    n = 0
    while True:
        # 确保可以请求成功
        try:
            res = requests.get(url=url, json=params, headers=headers, proxies=proxies).json()
            break
        except requests.exceptions.ProxyError:
            n += 1
            time.time(10)
            if n > 5:
                raise requests.exceptions.ProxyError('连接五次超时')
    # print(res)
    return res


def save(tweet, published, views, favorite_count, reply_count, retweet_count, relay):
    ws.append([tweet, published, views, favorite_count, reply_count, retweet_count, relay])


def parse_tweet(entries):
    for e in entries:
        if e['content']['entryType'] == 'TimelineTimelineItem':
            result = e['content']['itemContent']['tweet_results']['result']
            published = result['legacy']['created_at']
            try:
                # 如果是转发(不存在这个属性count)或者是本来就没有返回浏览量的
                views = result['views']['count']
                relay = ''
            except KeyError:
                try:
                    # 存在这个属性(retweeted_status_result)即为转发推文
                    result = result['legacy']['retweeted_status_result']['result']
                    try:
                        # 存在没有返回浏览量的情况
                        views = result['views']['count']
                        relay = ''
                    except KeyError:
                        views = ''
                        relay = '是'
                except KeyError:
                    views = ''
                    relay = ''
            tweet = result['legacy']['full_text']
            reply_count = result['legacy']['reply_count']
            retweet_count = int(result['legacy']['retweet_count']) + int(result['legacy']['quote_count'])
            favorite_count = result['legacy']['favorite_count']
            print('tweet-->', tweet)
            print('-' * 50)
            save(tweet, published, views, favorite_count, reply_count, retweet_count, relay)
        elif e['content']['cursorType'] == 'Top':
            # 上一页的curse值
            top_value = e['content']['value']
            # print(top_value)
        elif e['content']['cursorType'] == 'Bottom':
            global order
            global num
            num += len(entries) - 2
            order += 1
            # 下一页的curse值
            bottom_value = e['content']['value']
            print(bottom_value)
            print(f'第{order}页,累积{num}条', '-' * 50)
            return bottom_value


def parse(res):
    try:
        errors = res['errors']
    except KeyError:
        return ''
    instructions = res['data']['user']['result']['timeline_v2']['timeline']['instructions']
    for i in instructions:
        if i['type'] == 'TimelineAddEntries':
            entries = i['entries']
            return entries
        elif i['type'] == 'TimelinePinEntry':
            # 置顶推文
            pass


if __name__ == '__main__':
    start_time = time.time()
    userid = '44196397'
    res = request(userid=userid)
    entries = parse(res)
    if entries == '':
        print('该用户没有推文')
    else:
        bottom_value = parse_tweet(entries)
        while bottom_value:
            res = request(userid=userid, cursor=bottom_value)
            entries = parse(res)
            if entries == '':
                break
            if len(entries) == 2:
                break
            bottom_value = parse_tweet(entries)
    wb.save('Tweet.xlsx')
    print('耗时:', time.time() - start_time)
