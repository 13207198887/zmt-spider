from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from pykeyboard import PyKeyboard
import time
import os
import json


key = PyKeyboard()

# def run(*args):
#     usr, pwd, driver, article_id, title, content = args
def run():
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
    usr = '18523152354'
    pwd = ''
    vedio_name = '好漂亮的小姐姐Abeautifullittlesister姉loveTikTokGlobalVideoCommunity'
        
    driver.get("http://creator.miaopai.com/upload")

    #COOKIE登录
    driver.delete_all_cookies()
    # if os.path.exists(os.getcwd()+'\\utils\\miaopaicookie.json'):
    #     with open(os.getcwd()+'\\utils\\miaopaicookie.json', 'r', encoding='utf-8') as f:
    #单独调试的时候的路径
    if os.path.exists(os.path.dirname(os.getcwd())+'\\utils\\miaopaicookie.json'):
        with open(os.path.dirname(os.getcwd())+'\\utils\\miaopaicookie.json', 'r', encoding='utf-8') as f:
            for cookie in json.loads(f.read()):
                driver.add_cookie({
                    'domain': '.miaopai.com',
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'path': '/',
                    'expires': None
                })
            driver.get("http://creator.miaopai.com/upload")
    
    if driver.current_url == "http://creator.miaopai.com/login":
        elements_usrname = driver.find_element_by_xpath("//div[@class='login-form']//form/div[1]/input")
        elements_usrname.send_keys(usr)
        elements_pwd = driver.find_element_by_xpath("//div[@class='login-form']//form/div[2]/input")
        elements_pwd.send_keys(pwd)
        elements_login_submit = driver.find_element_by_xpath("//div[@class='login-form']//form/button")
        elements_login_submit.click()
        time.sleep(3)
        driver.get("http://creator.miaopai.com/upload")
        # with open(os.getcwd()+'\\utils\\miaopaicookie.json', 'w') as f:
        with open(os.path.dirname(os.getcwd())+'\\utils\\miaopaicookie.json', 'w') as f:
            f.write(json.dumps(driver.get_cookies()))
    elements_upload_video = driver.find_element_by_id("uploadVideo")
    elements_upload_video.click()
    # pic_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\\video\\'+str(article_id)+'.png'
    video_path = os.path.dirname(os.getcwd())+'\\video\\'+str(vedio_name)+'.mp4'
    print(video_path)
    key.tap_key(key.shift_key)
    key.type_string(video_path)
    key.tap_key(key.enter_key)
    key.tap_key(key.enter_key)
    time.sleep(3)
    #TODO:视频上传过程中的相关信息的修改
    