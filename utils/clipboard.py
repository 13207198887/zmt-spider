'''python操作系统内的剪切板'''

import win32clipboard as w
import win32con


def settext(aString):
    '''将文本写入剪切板'''
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()
    