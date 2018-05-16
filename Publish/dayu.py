from selenium import webdriver
from selenium.webdriver import ActionChains
from pykeyboard import PyKeyboard
import time
import os
import json


key = PyKeyboard()

def run(*args):
    driver, article_id, title, content = args
    '''发布流程
    进入文章发表页->填写文章标题->插入图片->添加本地图片->确认添加(自动关闭图片添加的窗口回到正文)->(暂时不填入图片描述)填写文章正文(此时已自动生成封面)->保存
    '''
    driver.get("https://mp.dayu.com/dashboard/article/write")

    #COOKIE登录
    driver.delete_all_cookies()
    if os.path.exists(os.getcwd()+'\\utils\\dayucookie.json'):
        with open(os.getcwd()+'\\utils\\dayucookie.json', 'r', encoding='utf-8') as f:
            for cookie in json.loads(f.read()):
                driver.add_cookie({
                    'domain': 'mp.dayu.com',
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'path': '/',
                    'expires': None
                })
            driver.get("https://mp.dayu.com/dashboard/article/write")

    if driver.current_url == "https://mp.dayu.com/?redirect_url=%2Fdashboard%2Farticle%2Fwrite":
        Flag = True
        driver.get("https://mp.dayu.com/mobile/index")
        time.sleep(5)
        driver.switch_to.frame(driver.find_element_by_xpath("//div[@class='loginPage-mobileLogin_body']//iframe"))
        elements_usr = driver.find_element_by_id("login_name")
        elements_usr.send_keys("18523152354")
        elements_pwd = driver.find_element_by_id("password")
        elements_pwd.send_keys("")
        # elements_slideBtn = driver.find_element_by_class_name("btn_slide") #PC下的定位
        #判断是否需要滑块验证
        if is_element_exist(driver, ".slider"):
            elements_slideBtn = driver.find_element_by_xpath("//div[@class='slider']//div[@class='button']") 
            action = ActionChains(driver)
            action.click_and_hold(elements_slideBtn).perform()
            action.reset_actions()
            action.move_by_offset(1322, 0).perform()
            time.sleep(5)
            #判断是否需要输入验证码
            if is_element_exist(driver, ".icon-warn"):
                QRCode_Url = driver.find_element_by_xpath("//div[@class='textbox']//img").get_attribute('src')
                ocr = OcrUtil()
                #TODO:处理百度识别出错的情况
                QRCode = ocr.get_image_verfy_code(QRCode_Url)
                elements_insertCode = driver.find_element_by_xpath("//div[@class='textbox']//input")
                elements_insertCode.send_keys(QRCode)
                elements_ok = driver.find_element_by_class_name("btn-ok")
                elements_ok.click()
                time.sleep(3)
                #判断验证码是否正确(不正确的话暂时手动输入)
                while True:
                    elements_login = driver.find_element_by_id("submit_btn")
                    try:
                        elements_login.click()
                        Flag = False
                        break
                    except:
                        elements_insertCode.send_keys(input("输入验证码："))
                        elements_ok.click()
                        time.sleep(3) 
                time.sleep(2)
        if Flag:               
            elements_login = driver.find_element_by_id("submit_btn")
            elements_login.click()
            time.sleep(5)
        with open(os.getcwd()+'\\utils\\dayucookie.json', 'w') as f:
            f.write(json.dumps(driver.get_cookies()))
    driver.get("https://mp.dayu.com/dashboard/article/write")
    elements_title = driver.find_element_by_class_name("article-write_box-title-input")
    elements_title.send_keys(title)
    #插入图片
    elements_insert_pic = driver.find_element_by_id("edui14_body")
    elements_insert_pic.click()
    elements_select_pic = driver.find_element_by_class_name("webuploader-element-invisible")
    # elements_select_pic.click() #此处的dom无法点击，换用action点击
    ActionChains(driver).move_to_element(elements_select_pic).click(elements_select_pic).perform()
    time.sleep(2)
    #获取本地封面的路径
    pic_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\\cover\\'+str(article_id)+'.png'
    #TODO:这里有bug,中文下会输入英文。英文下会输入中文
    key.tap_key(key.shift_key)
    key.type_string(pic_path)
    key.tap_key(key.enter_key)
    key.tap_key(key.enter_key)
    time.sleep(2)
    elements_confirm_addPic = driver.find_element_by_xpath("//div[@class='article-material-image-dialog_root']//button[2]")
    #等待上传完毕
    time.sleep(5)
    elements_confirm_addPic.click()
    time.sleep(2)
    #driver.switch_to_window(driver.window_handles[0])
    #填写正文，此时图片已插入frame
    # driver.switch_to.frame("ueditor_0")
    # elements_content = driver.find_element_by_xpath("//body[@class='view']//p[@class='empty']") 
    # elements_content.send_keys(content)
    driver.switch_to.active_element.send_keys(content)
    driver.switch_to.default_content()
    elements_publish = driver.find_element_by_xpath("//div[@class='w-btn-toolbar']/button[4]")
    #辅助封面自动生成(利用js指令将页面下拉到底部)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    #文本太长的情况下需要时间   
    time.sleep(70)
    elements_publish.click()
    time.sleep(10)
    #处理弹框
    try:
        key.tap_key(key.enter_key)
    except:
        pass

'''
辅助方法
'''
def is_element_exist(driver, css):
    '''判断元素是否存在'''
    s = driver.find_elements_by_css_selector(css_selector=css)
    if len(s) == 0:
        return False
    elif len(s) == 1:
        return True
    else:
        return False

'''
百度OCR'''
from aip import AipOcr
import urllib
from urllib import request

APP_ID = '10689488'
API_KEY = 'UtCZwstXn3yl1UDqAK70vTMu'
SECRET_KEY = 'mXEgrdDygnY3xRGA7xY6dvGvC7A5qD6B'


class OcrUtil(object):

    # 通过链接读取图片
    def open_url_content(self,url):
        return urllib.request.urlopen(url).read()

    def get_image_verfy_code(self, url):
        try:
            aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
            result = aipOcr.basicGeneral(self.open_url_content(url))
            verification_code = result.get('words_result')[0]['words']
            return verification_code
        except:
            return "0000"


if __name__ == "__main__":
    run()
    
