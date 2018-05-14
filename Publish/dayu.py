from selenium import webdriver
from selenium.webdriver import ActionChains
from pykeyboard import PyKeyboard
import time
import os

# 进入浏览器设置
options = webdriver.ChromeOptions()
# 设置中文
options.add_argument('lang=zh_CN.UTF-8')
# 更换头部
'''登陆时将请求头设置成手机代理防止被检测出来,登录请求的URL也用手机web版登录然后跳转回正常页面'''
options.add_argument('user-agent: "Mozilla/5.0 (Android 6.0.1; Mo…43.0) Gecko/43.0 Firefox/43.0"')
driver = webdriver.Chrome(chrome_options=options)
#driver = webdriver.Firefox()
driver.maximize_window()

key = PyKeyboard()

def dayu(title, pic_path, content):
    '''发布流程
    进入文章发表页->填写文章标题->插入图片->添加本地图片->确认添加(自动关闭图片添加的窗口回到正文)->(暂时不填入图片描述)填写文章正文(此时已自动生成封面)->保存
    '''
    driver.get("https://mp.dayu.com/dashboard/article/write")
    if driver.current_url == "https://mp.dayu.com/?redirect_url=%2Fdashboard%2Farticle%2Fwrite":
        driver.get("https://mp.dayu.com/mobile/index")
        time.sleep(5)
        driver.switch_to.frame(driver.find_element_by_xpath("//div[@class='loginPage-mobileLogin_body']//iframe"))
        elements_usr = driver.find_element_by_id("login_name")
        elements_usr.send_keys("18523152354")
        elements_pwd = driver.find_element_by_id("password")
        elements_pwd.send_keys("")
        # elements_slideBtn = driver.find_element_by_class_name("btn_slide") #PC下的定位
        #判断是否需要滑块验证
        if is_element_exist(".slider"):
            elements_slideBtn = driver.find_element_by_xpath("//div[@class='slider']//div[@class='button']") 
            action = ActionChains(driver)
            action.click_and_hold(elements_slideBtn).perform()
            action.reset_actions()
            action.move_by_offset(1322, 0).perform()
            time.sleep(5)
            #判断是否需要输入验证码
            if is_element_exist(".icon-warn"):
                QRCode_Url = driver.find_element_by_xpath("//div[@class='textbox']//img").get_attribute('src')
                ocr = OcrUtil()
                #TODO:处理百度识别出错的情况
                QRCode = ocr.get_image_verfy_code(QRCode_Url)
                elements_insertCode = driver.find_element_by_xpath("//div[@class='textbox']//input")
                elements_insertCode.send_keys(QRCode)
                elements_ok = driver.find_element_by_class_name("btn-ok")
                elements_ok.click()
                time.sleep(3)
        elements_login = driver.find_element_by_id("submit_btn")
        elements_login.click()
        time.sleep(5)
    driver.get("https://mp.dayu.com/dashboard/article/write")
    elements_title = driver.find_element_by_class_name("article-write_box-title-input")
    elements_title.send_keys(title)
    #插入图片
    elements_insert_pic = driver.find_element_by_id("edui14_body")
    elements_insert_pic.click()
    elements_select_pic = driver.find_element_by_xpath("//div[@class='webuploader-container']/button")
    elements_select_pic.click()
    key.type_string(pic_path)
    key.enter_key()
    #等待上传完毕
    elements_confirm_addPic = driver.find_element_by_xpath("//div[@class='article-material-image-dialog_root']/button[2]")
    elements_confirm_addPic.click()
    #填写正文，此时图片已插入frame
    driver.switch_to.frame("ueditor_0")
    elements_content = driver.find_element_by_xpath("/body[@class='view simple-ui']/p[3]")
    elements_content.send_keys(content)
    driver.switch_to.default_content()
    elements_publish = driver.find_element_by_xpath("//div[@class='article-write_box-opt_msgNum']/button[4]")
    elements_publish.click()

'''
辅助方法
'''
def is_element_exist(css):
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
        aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        result = aipOcr.basicGeneral(self.open_url_content(url))
        try:
            verification_code = result.get('words_result')[0]['words']
            return verification_code
        except:
            return None





title = "NASA plans to send mini-helicopter to Mars"
pic_path = "file:///"+os.getcwd()+"/test.jpeg"
content = "It is part of the US space agency 2020 mission to place a next-generation rover on the Martian surface and will mark the first time such an aircraft will be used on another planet.Known as the Mars Helicopter, the remote-controlled device weighs less than four pounds (1.8kg) and its blades spin at almost 3,000rpm, roughly 10 times the rate employed by helicopters on Earth.NASA officials said the aircraft will reach the Red Planet's surface attached to the Mars 2020 rover that aims to carry out geological studies and ascertain the habitability of the Martian environment.NASA has a proud history of firsts, said NASA administrator Jim Bridenstine.The idea of a helicopter flying the skies of another planet is thrilling."
dayu(title, pic_path, content)
