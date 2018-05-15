from Publish import dayu
from utils.Crawl_article import spider_tc, spider_reuters

while True:
    article_id, title, content = spider_tc()
    if article_id and title and content:
        dayu.run(article_id, title, content)
    reuters_data = spider_reuters()
    if reuters_data:
        for data in reuters_data:
            article_id = data['article_id']
            title = data['title']
            content = data[' content']
            dayu.run(article_id, title, content)

    



'''
TODO: 多进程爬取文章并发布,判断浏览器是否已开启，已开启的话则跳过新建一个浏览器进程节省开销
特别是 循环发布的时候

优化: 直接把所有要发布的文章集合到一个列表中，然后以列表的形式传参给平台[dayu.py],循环发布，每发布完一篇就重进写文章的页面中
'''