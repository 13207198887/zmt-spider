import urllib
from urllib import request
import re
import os
import subprocess


def download_video(share_url):
    '''通过分享链接下载无水印视频
    param: share_url->分享链接
    '''
    # header = {
    #     "referer": share_url,
    #     "Host": "p3.pstatp.com",
    #     #"user-agent": "Mozilla/5.0 (Android 6.0.1; Mo…43.0) Gecko/43.0 Firefox/43.0"
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
    # }
    res = urllib.request.urlopen(share_url).read().decode('utf-8')
    video_title = re.findall(r'<title>(.*?)</title>', res)[0]
    print(video_title)
    head_url = re.findall(r'.*? property="og:video:secure_url" content="(.*?)">.*?', res, re.I|re.S|re.M)[0]
    download_url = head_url.replace('playwm', 'play').replace('&amp;', '&').replace('line=0', 'line=1')
    video_name = "".join(re.findall(r'[\u4e00-\u9fa5_a-zA-Z0-9]+', video_title))+'.mp4'
    print(video_name)
    download_cli(download_url, video_name)

def download_cli(url, fname):
    '''调用ffmpeg进行视频下载
    param: url->下载链接  fname->下载文件名
    '''
    ffmpeg_path = os.path.dirname(os.getcwd())+"\\env\\ffmpeg"
    download_path = os.path.dirname(os.getcwd())+"\\vedio\\"+fname
    print('Download==> {}'.format(url))
    subprocess.call([ffmpeg_path, '-i', url, '-f', 'mp4', download_path])


download_video("https://www.tiktokv.com/i18n/share/video/6544720741055597825/?region=cn&mid=6429187299342453505")
