import json
import urllib
from urllib import request
import re
import pymongo

import translate

def spider_tc():
    tc_url = "https://techcrunch.com/wp-json/tc/v1/magazine?page=1&_embed=true&_envelope=true&categories=449557028"
    header = {
        "referer": "https://techcrunch.com/mobile/",
        "upgrade-insecure-requests": 1,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36"
    }
    req = urllib.request.Request(tc_url, headers=header)
    res = urllib.request.urlopen(req).read()
    js_result = json.loads(res)
    for article in js_result['body']:
        link = article['guid']['rendered']
        title = translate.TranslateByGoogle(article['title']['rendered']) 
        content = translate.TranslateByGoogle(re.sub(r'</?\w+[^>]*>', '', article['content']['rendered']) ) 
        db.articles.insert({ "link": link, "title": title, "content": content })
        print(link)

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['zmt']
spider_tc()