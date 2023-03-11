# import requests
# import re
#
#
# class Twitter:
#     def __init__(self):
#         self.url = "https://api.twitter.com/graphql/73BM9FU1mPITScnhs6iXug/UserTweets"
#
#     def request(self, user_id, cursor=""):
#         params = {
#             "variables": f"{{\"userId\":\"{user_id}\",\"count\":40,\"includePromotedContent\":true,\"withQuickPromoteEligibilityTweetFields\":true,\"withSuperFollowsUserFields\":true,\"withDownvotePerspective\":false,\"withReactionsMetadata\":false,\"withReactionsPerspective\":false,\"withSuperFollowsTweetFields\":true,\"withVoice\":true,\"withV2Timeline\":true}}",
#             "features": "{\"responsive_web_twitter_blue_verified_badge_is_enabled\":true,\"responsive_web_graphql_exclude_directive_enabled\":false,\"verified_phone_label_enabled\":false,\"responsive_web_graphql_timeline_navigation_enabled\":true,\"responsive_web_graphql_skip_user_profile_image_extensions_enabled\":false,\"tweetypie_unmention_optimization_enabled\":true,\"vibe_api_enabled\":true,\"responsive_web_edit_tweet_api_enabled\":true,\"graphql_is_translatable_rweb_tweet_is_translatable_enabled\":true,\"view_counts_everywhere_api_enabled\":true,\"longform_notetweets_consumption_enabled\":true,\"tweet_awards_web_tipping_enabled\":false,\"freedom_of_speech_not_reach_fetch_enabled\":false,\"standardized_nudges_misinfo\":true,\"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled\":false,\"interactive_text_enabled\":true,\"responsive_web_text_conversations_enabled\":false,\"longform_notetweets_richtext_consumption_enabled\":false,\"responsive_web_enhance_cards_enabled\":false}"
#         }
#         if cursor != "":
#             params["variables"] = re.sub('"count":40,', f'"count":40,"cursor":"{cursor}",', params["variables"])
#
#
# if __name__ == "__main__":
#     headers = {
#         'authority': 'api.twitter.com',
#         'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
#         'origin': 'https://twitter.com',
#         'referer': 'https://twitter.com/',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
#     }
#     proxies = {
#         'https': 'http://127.0.0.1:10809', 'http': 'http://127.0.0.1:10809'
#     }
#     proxies = {'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'}
#     response = requests.post('https://api.twitter.com/1.1/guest/activate.json', proxies=proxies, headers=headers).json()
#     # response = requests.post('https://api.twitter.com/1.1/jot/client_event.json',headers=headers,proxies=proxies)
#     print(response)
