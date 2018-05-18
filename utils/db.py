import sqlite3
import os

def init_db():
    '''初始化本地数据库
    '''
    conn = sqlite3.connect(os.getcwd()+'\\utils\\articles.db')
    return conn

def exist_article(link):
    '''查询文章是否收录'''
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("select * from articles where link='%s'" % link )
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
            "insert into articles (link, article_id, title, content) values ('%s', '%s', '%s', '%s')" % (link, str(article_id), title, content)
        )
        conn.commit()
    except:
        conn.rollback()
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
    '''添加已发布的文章link
    table_name: 表名也就是平台的名字
    '''
    conn = init_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "insert into '%s' (article_link) values('%s')" % (table_name, link)
        )
        conn.commit()
    except:
        conn.rollback()
        print("该文章已发布但无法入库：%s" % link )
    conn.close()

def whether_published(table_name, link):
    '''根据link查询该文章是否已发布
    table_name: 表名也就是平台的名字
    '''
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("select * from '%s' where link='%s'" % (table_name, link))
    values = cursor.fetchone()
    if values:
        print("该文章已发布过了:%s" % link)
        return True
    else:
        return False

