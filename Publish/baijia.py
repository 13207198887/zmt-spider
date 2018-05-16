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


key = PyKeyboard

def run():
    driver = init_driver()
    driver.get("https://baijiahao.baidu.com/builder/rc/edit?type=news&app_id=1600282401631826")

    #COOKIE登录
    driver.delete_all_cookies()
    # if os.path.exists(os.getcwd()+'\\utils\\baijiacookie.json'):
    #     with open(os.getcwd()+'\\utils\\baijiacookie.json', 'r', encoding='utf-8') as f:
    if os.path.exists(os.path.dirname(os.getcwd())+'\\utils\\baijiacookie.json'):
        with open(os.path.dirname(os.getcwd())+'\\utils\\baijiacookie.json', 'r', encoding='utf-8') as f:
            for cookie in json.loads(f.read()):
                driver.add_cookie({
                    'domain': '.baidu.com',
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'path': '/',
                    'expires': None
                })
            driver.get("https://baijiahao.baidu.com/builder/rc/edit?type=news&app_id=1600282401631826")
    
    if driver.current_url == "https://baijiahao.baidu.com/builder/author/register/index":
        driver.get("https://passport.baidu.com")
        elements_select_login = driver.find_element_by_id("TANGRAM__PSP_3__footerULoginBtn")
        elements_select_login.click()
        elements_usrname = driver.find_element_by_id("TANGRAM__PSP_3__userName")
        elements_usrname.send_keys("18523152354")
        elements_pwd = driver.find_element_by_id("TANGRAM__PSP_3__password")
        elements_pwd.send_keys("")
        elements_login_submit = driver.find_element_by_id("TANGRAM__PSP_3__submit")
        elements_login_submit.click()
        time.sleep(3)
        driver.get("https://baijiahao.baidu.com/builder/rc/home")
        #with open(os.getcwd()+'\\utils\\baijiacookie.json', 'w') as f:
        with open(os.path.dirname(os.getcwd())+'\\utils\\baijiacookie.json', 'w') as f:
            f.write(json.dumps(driver.get_cookies()))
    driver.get("https://baijiahao.baidu.com/builder/rc/edit?type=news&app_id=1600282401631826")
    elements_title = driver.find_element_by_xpath("//div[@class='input-box']//input")
    elements_title.send_keys(title)
    time.sleep(3)
    elements_insert_pic = driver.find_element_by_id("edui20_body")
    elements_insert_pic.click()
    driver.switch_to.frame("edui14_iframe")
    time.sleep(3)
    elements_select_pic = driver.find_element_by_id("filePickerReady")
    elements_select_pic.click()
    pic_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\\cover\\'+str(article_id)+'.png'
    print(pic_path)
    #key.tap_key(key.shift_key)
    key.type_string(pic_path)
    key.tap_key(key.enter_key)
    key.tap_key(key.enter_key)
    time.sleep(3)
    elements_confirm_addPic = driver.find_element_by_id("edui19_body")
    elements_confirm_addPic.click()
    driver.switch_to.active_element.send_keys(content)
    driver.switch_to.default_content()
    elements_cover_radio = driver.find_element_by_xpath("//div[@class='cover-radio-group']//lable[3]/span/input")
    elements_cover_radio.click()
    #TODO:领域的选择暂时跳过,页面有BUG
    #下拉菜单处理，需要引入Select
    #elements_field_select = Select(driver.find_element_by_class_name("ant-select-selection__rendered"))
    elements_publish = driver.find_element_by_xpath("//span[@class='op-list']//button[3]")
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
