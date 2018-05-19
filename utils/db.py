import sqlite3
import os

#===============================================文章=======================================
def init_db():
    '''初始化本地数据库
    '''
    conn = sqlite3.connect(os.getcwd()+'\\utils\\articles.db')
    return conn

def exist_article(link):
    '''查询文章是否收录'''
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("select * from articles where link='%s'" % link)
    values = cursor.fetchone()
    if values:
        return True
    else:
        return False

def add_article(link, article_id, title, content):
    '''添加新的文章'''
    conn = init_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "insert into articles (link, article_id, title, content) values (?, ?, ?, ?)" , (link, str(article_id), title, content)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error：%s" % e)
        print("存入数据库失败：%s" % link )
    conn.commit()
    conn.close()

def get_articles():
    '''从数据库中取出数据'''
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("select * from articles")
    values = cursor.fetchall()
    return values

def published_article(table_name, link):
    '''添加已发布的文章link,并清空对应文章的内容
    table_name: 表名也就是平台的名字
    '''
    conn = init_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "insert into '%s' (article_link) values ('%s')" % (table_name, link)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error：%s" % e)
        print("该文章已发布但无法入库：%s" % link )
    else:
        cursor = conn.cursor()
        #已发布的文章link记录成功后清空articles表中对应的文章content，减少db文件体积
        try:
            cursor.execute(
                "update articles set content = '%s' where link = '%s'" % ("已发布", link)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            print("Error：%s" % e)
            print("该文章清空内容失败：%s" % link )
    conn.close()

def whether_published(table_name, link):
    '''根据link查询该文章是否已发布
    table_name: 表名也就是平台的名字
    '''
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("select * from '%s' where article_link ='%s'" % (table_name, link))
    values = cursor.fetchone()
    if values:
        print("该文章已发布过了:%s" % link)
        return True
    else:
        return False


#============================================视频===========================================
def init_videoDB():
    '''初始化本地视频下载链接数据库
    '''
    conn = sqlite3.connect(os.getcwd()+'\\utils\\videos.db')
    return conn

def download_video(link):
    '''添加已下载的视频link
    param: link->视频下载链接
    '''
    conn = init_videoDB()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "insert into videos (download_link) values ('%s')" % link
        )
        conn.commit()
        print("该视频下载链接成功入库：%s" % link)
    except Exception as e:
        conn.rollback()
        print("Error：%s" % e)
        print("该链接视频已下载但无法入库该link：%s" % link )
    conn.close()


def whether__download(link):
    '''查询视频是否已经下载过了'''
    conn = init_videoDB()
    cursor = conn.cursor()
    cursor.execute("select * from videos where download_link='%s'" % link)
    values = cursor.fetchone()
    if values:
        print("该视频已下载过了：%s" % link)
        return True
    else:
        return False