from Publish import dayu
from utils.Crawl_article import spider_tc, spider_reuters, spider_techradar

from selenium import webdriver


def init_driver():
    '''初始化浏览器'''
    #===========================Chrome=================
    #进入浏览器设置
    options = webdriver.ChromeOptions()
    # 设置中文
    options.add_argument('lang=zh_CN.UTF-8')
    # 更换头部
    '''登陆时将请求头设置成手机代理防止被检测出来,登录请求的URL也用手机web版登录然后跳转回正常页面'''
    options.add_argument('user-agent: "Mozilla/5.0 (Android 6.0.1; Mo…43.0) Gecko/43.0 Firefox/43.0"')
    #不显示前台界面
    #options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    #driver = webdriver.Firefox()
    driver.maximize_window()
    return driver


driver = init_driver()
while True:
    # article_id, title, content = spider_tc()
    # if article_id and title and content:
    #     dayu.run(article_id, title, content)
    # reuters_data = spider_reuters()
    # if reuters_data:
    #     for data in reuters_data:
    #         article_id = data['article_id']
    #         title = data['title']
    #         content = data['content']
    #         dayu.run(driver, article_id, title, content)
    techradar_data = spider_techradar()
    if techradar_data:
        for data in techradar_data:
            try:
                article_id = data['article_id']
                title = data['title']
                content = data['content']
                dayu.run(driver, article_id, title, content)
            except:
                continue

    



'''
TODO: 多进程爬取文章并发布,判断浏览器是否已开启，已开启的话则跳过新建一个浏览器进程节省开销
特别是 循环发布的时候

优化: 直接把所有要发布的文章集合到一个列表中，然后以列表的形式传参给平台[dayu.py],循环发布，每发布完一篇就重进写文章的页面中
'''