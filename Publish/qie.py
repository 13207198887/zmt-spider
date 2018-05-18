from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from pykeyboard import PyKeyboard
import time
import os
import json


key = PyKeyboard()

def run(*args):
    usr, pwd, driver, article_id, title, content = args

    #处理弹框
    try:
        key.tap_key(key.enter_key)
    except:
        pass
        
    driver.get("https://om.qq.com/article/articlePublish")

    #COOKIE登录
    driver.delete_all_cookies()
    if os.path.exists(os.getcwd()+'\\utils\\baijiacookie.json'):
        with open(os.getcwd()+'\\utils\\baijiacookie.json', 'r', encoding='utf-8') as f:
    #单独调试的时候的路径
    # if os.path.exists(os.path.dirname(os.getcwd())+'\\utils\\qiecookie.json'):
    #     with open(os.path.dirname(os.getcwd())+'\\utils\\qiecookie.json', 'r', encoding='utf-8') as f:
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
        # driver.get("https://m.om.qq.com/mobile/login")
        # elements_usrname = driver.find_element_by_xpath("//form[@class='form-control']/div[1]/input")
        # elements_usrname.send_keys("201417160@qq.com")
        # elements_pwd = driver.find_element_by_xpath("//form[@class='form-control']/div[2]/input")
        # elements_pwd.send_keys("")
        # elements_remberme = driver.find_element_by_class_name("icon-login-checkbox")
        # elements_remberme.click()
        # elements_login_submit = driver.find_element_by_xpath("//div[@class='login-submit']/button")
        # elements_login_submit.click()
        #driver.get("https://om.qq.com/article/index")

        key.tap_key(key.tab_key)
        key.tap_key(key.tab_key)
        key.tap_key(key.tab_key)
        driver.switch_to.active_element.send_keys(usr)
        key.tap_key(key.tab_key)
        driver.switch_to.active_element.send_keys(pwd)
        key.tap_key(key.enter_key)
        time.sleep(5)

        driver.get("https://om.qq.com/article/articlePublish")
        with open(os.getcwd()+'\\utils\\qiecookie.json', 'w') as f:
        # with open(os.path.dirname(os.getcwd())+'\\utils\\qiecookie.json', 'w') as f:
            f.write(json.dumps(driver.get_cookies()))
    # elements_title = driver.find_element_by_xpath("//div[@class='form-group-title']")
    # ActionChains(driver).move_to_element(elements_title).click(elements_title).perform()
    # elements_title_count = (driver.find_element_by_xpath("//label[@class='input-control-title']/div").text).split('/')[0]
    #--------------------------------------------------------------------
    # elements_title_count = driver.find_element_by_xpath("//label[@class='input-control-title']/div")
    # ActionChains(driver).move_to_element(elements_title_count).click(elements_title_count).perform()
    # elements_title_count_num = (elements_title_count.text).split('/')[0]
    # if int(elements_title_count_num) != 0:
    #     for _ in range(int(elements_title_count_num)):
    #         key.tap_key(key.cancel_key)
    # driver.switch_to.active_element.send_keys(title)
    for _ in range(25):
        key.tap_key(key.tab_key)
    key.tap_key(key.space_key)
    driver.switch_to.active_element.send_keys(title)
    time.sleep(3)
    elements_insert_pic = driver.find_element_by_id("edui8_body")
    elements_insert_pic.click()
    elements_select_pic = driver.find_element_by_class_name("upload-block-media")
    elements_select_pic.click()
    pic_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\\cover\\'+str(article_id)+'.png'
    print(pic_path)
    key.tap_key(key.shift_key)
    time.sleep(1)
    key.type_string(pic_path)
    key.tap_key(key.enter_key)
    time.sleep(1)
    key.tap_key(key.enter_key)
    time.sleep(5)
    elements_confirm_addPic = driver.find_element_by_class_name("layui-layer-btn0")
    elements_confirm_addPic.click()
    driver.switch_to.active_element.send_keys(content)
    driver.switch_to.default_content()
    #领域的选择默认
    # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    # elements_field_select = driver.find_element_by_class_name("item")
    # elements_field_select.click()
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
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


if __name__ == "__main__":
    run()
    
