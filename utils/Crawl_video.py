import urllib
from urllib import request
import re
import os
import subprocess
import json


class Tiktok:
    '''下载国际版抖音的视频，无水印
    根据分享的链接下载; 下载我的收藏
    '''

    def share_download(self, share_url):
        '''通过分享链接下载无水印视频
        param: share_url->分享链接
        '''
        res = urllib.request.urlopen(share_url).read().decode('utf-8')
        video_title = re.findall(r'<title>(.*?)</title>', res)[0]
        print(video_title)
        head_url = re.findall(r'.*? property="og:video:secure_url" content="(.*?)">.*?', res, re.I|re.S|re.M)[0]
        download_url = head_url.replace('playwm', 'play').replace('&amp;', '&').replace('line=0', 'line=1')
        video_name = "".join(re.findall(r'[\u4e00-\u9fa5_a-zA-Z0-9]+', video_title))+'.mp4'
        print(video_name)
        self.download_cli(download_url, video_name)

    def favorite_download(self):
        '''下载我的收藏
        收藏视频列表https://www.tiktokv.com/aweme/v1/aweme/favorite/?user_id=6535937954585051138{&max_cursor=0&count=2}
        我的UID:6557148225815494657
        '''
        url = "https://www.tiktokv.com/aweme/v1/aweme/favorite/?user_id=6535937954585051138"
        json_res = urllib.request.urlopen(url)
        values = json.loads(json_res.read())
        for value in values['aweme_list']:
            video_url = value['video']['play_addr']['url_list'][0]
            download_url = video_url.replace('playwm', 'play').replace('&amp;', '&').replace('line=0', 'line=1')
            #根据需要看是否需要下载封面图
            #cover_url = value['video']['cover']['url_list'][0]
            #video_desc = value['desc'] 可能没有描述和标题
            self.download_cli(download_url, "你尽管点开，不好看算我输.mp4")


    def download_cli(self, url, fname):
        '''调用ffmpeg进行视频下载
        param: url->下载链接  fname->下载文件名
        '''
        ffmpeg_path = os.path.dirname(os.getcwd())+"\\env\\ffmpeg"
        download_path = os.path.dirname(os.getcwd())+"\\vedio\\"+fname
        print('Download==> {}'.format(url))
        subprocess.call([ffmpeg_path, '-i', url, '-f', 'mp4', download_path])


#tiktok("https://www.tiktokv.com/i18n/share/video/6544720741055597825/?region=cn&mid=6429187299342453505")
