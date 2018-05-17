from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from pykeyboard import PyKeyboard
import time
import os
import json

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
    # driver = webdriver.Firefox()
    driver.maximize_window()
    return driver


key = PyKeyboard()

def run():
    driver = init_driver()
    driver.get("https://om.qq.com/article/articlePublish")

    #COOKIE登录
    driver.delete_all_cookies()
    # if os.path.exists(os.getcwd()+'\\utils\\baijiacookie.json'):
    #     with open(os.getcwd()+'\\utils\\baijiacookie.json', 'r', encoding='utf-8') as f:
    if os.path.exists(os.path.dirname(os.getcwd())+'\\utils\\qiecookie.json'):
        with open(os.path.dirname(os.getcwd())+'\\utils\\qiecookie.json', 'r', encoding='utf-8') as f:
            for cookie in json.loads(f.read()):
                driver.add_cookie({
                    'domain': '.qq.com',
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'path': '/',
                    'expires': None
                })
            driver.get("https://om.qq.com/article/articlePublish")

    if driver.current_url == "https://om.qq.com/userAuth/index":
        driver.get("https://m.om.qq.com/mobile/login")
        elements_usrname = driver.find_element_by_xpath("//form[@class='form-control']/div[1]/input")
        elements_usrname.send_keys("18523152354")
        elements_pwd = driver.find_element_by_xpath("//form[@class='form-control']/div[2]/input")
        elements_pwd.send_keys("")
        elements_remberme = driver.find_element_by_class_name("icon-login-checkbox")
        elements_remberme.click()
        elements_login_submit = driver.find_element_by_xpath("//div[@class='login-submit']/button")
        elements_login_submit.click()
        time.sleep(3)
        driver.get("https://om.qq.com/article/index")
        #with open(os.getcwd()+'\\utils\\qiecookie.json', 'w') as f:
        with open(os.path.dirname(os.getcwd())+'\\utils\\qiecookie.json', 'w') as f:
            f.write(json.dumps(driver.get_cookies()))
    driver.get("https://om.qq.com/article/articlePublish")
    elements_title = driver.find_element_by_xpath("//label[@class='input-control-title']//input")
    elements_title.send_keys(title)
    time.sleep(3)
    elements_insert_pic = driver.find_element_by_id("edui8_body")
    elements_insert_pic.click()
    elements_select_pic = driver.find_element_by_class_name("upload-block-media")
    elements_select_pic.click()
    pic_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\\cover\\'+str(article_id)+'.png'
    print(pic_path)
    key.tap_key(key.shift_key)
    key.type_string(pic_path)
    key.tap_key(key.enter_key)
    key.tap_key(key.enter_key)
    time.sleep(5)
    elements_confirm_addPic = driver.find_element_by_class_name("layui-layer-btn0")
    elements_confirm_addPic.click()
    driver.switch_to.active_element.send_keys(content)
    driver.switch_to.default_content()
    elements_field_select = driver.find_element_by_class_name("item")
    elements_field_select.click()
    elements_publish = driver.find_element_by_xpath("//div[@id='mod-actions']//button[2]")
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(20)
    elements_publish.click()
    time.sleep(10)
    #处理弹框
    try:
        key.tap_key(key.enter_key)
    except:
        pass


title = "小米公司又出了一款新品"
content = "this is a test ,nixinbuxin"
article_id = "test"
run()
