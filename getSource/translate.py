import execjs  
import urllib.request   
    
class Py4Js():    
        
    def __init__(self):    
        self.ctx = execjs.compile("""  
        function TL(a) {  
        var k = "";  
        var b = 406644;  
        var b1 = 3293161072;  
          
        var jd = ".";  
        var $b = "+-a^+6";  
        var Zb = "+-3^+b+-f";  
      
        for (var e = [], f = 0, g = 0; g < a.length; g++) {  
            var m = a.charCodeAt(g);  
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),  
            e[f++] = m >> 18 | 240,  
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,  
            e[f++] = m >> 6 & 63 | 128),  
            e[f++] = m & 63 | 128)  
        }  
        a = b;  
        for (f = 0; f < e.length; f++) a += e[f],  
        a = RL(a, $b);  
        a = RL(a, Zb);  
        a ^= b1 || 0;  
        0 > a && (a = (a & 2147483647) + 2147483648);  
        a %= 1E6;  
        return a.toString() + jd + (a ^ b)  
    };  
      
    function RL(a, b) {  
        var t = "a";  
        var Yb = "+";  
        for (var c = 0; c < b.length - 2; c += 3) {  
            var d = b.charAt(c + 2),  
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),  
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;  
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d  
        }  
        return a  
    }  
    """)    
            
    def getTk(self,text):    
        return self.ctx.call("TL",text)  


def open_url(url):      
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}        
    req = urllib.request.Request(url = url,headers=headers)      
    response = urllib.request.urlopen(req)      
    data = response.read().decode('utf-8')      
    return data      
      
def translate(content,tk):      
    if len(content) > 4891:      
        print("翻译的长度超过限制！！！")      
        return       
          
    content = urllib.parse.quote(content)      
          
    url = "http://translate.google.cn/translate_a/single?client=t"+ "&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca"+"&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1"+"&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s"%(tk,content)      
          
    #返回值是一个多层嵌套列表的字符串形式，解析起来还相当费劲，写了几个正则，发现也很不理想，    
    #后来感觉，使用正则简直就是把简单的事情复杂化，这里直接切片就Ok了      
    result = open_url(url)      
    return result
    # end = result.find("\",")      
    # if end > 4:      
    #     print(result[4:end])      
      
def main(en_text):      
    js = Py4Js()      
    tk = js.getTk(en_text)      
    return translate(en_text,tk)      









#================== V2================
from http import client
import hashlib
import urllib
from urllib import request
from html.parser import HTMLParser

import random
import json
import re

agent = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}

def TranslateByBaidu(text,fromLang = 'auto',toLang = 'zh'):
    appid = "20180513000158179"
    secretKey = "3Y_muSFsaVLh9YGvk2gT"
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = text
    salt = random.randint(32768, 65536)

    sign = appid+q+str(salt)+secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode('utf-8'))
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.request.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
     
    try:
        httpClient = client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        #response是HTTPResponse对象
        response = httpClient.getresponse()
        result = response.read()
        data = json.loads(result)
        return data["trans_result"][0]["dst"]
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()



def unescape(text):
    parsers = HTMLParser()
    return (parsers.unescape(text))


def TranslateByGoogle(text, fromLang="auto", toLang="zh-CN"):
    base_link = "http://translate.google.cn/m?hl=%s&sl=%s&q=%s"
    text = urllib.request.quote(text)
    link = base_link % (toLang, fromLang, text)
    request = urllib.request.Request(link, headers=agent)
    try:
        raw_data = urllib.request.urlopen(request).read()
        data = raw_data.decode("utf-8")
        expr = r'class="t0">(.*?)<'
        re_result = re.findall(expr, data)
        if (len(re_result) == 0):
            result = ""
        else:
            result = unescape(re_result[0])
        return (result)
    except Exception as e:
        print(e)