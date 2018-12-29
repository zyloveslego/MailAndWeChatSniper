import itchat
from itchat.content import *

import re
import datetime

# version1.0 如果群收到的消息里，有想要的信息，则在filehelper里提醒


# 搜索字符串
def stringMatch(text):
    bt = 'rmb|人民币|dollar|美元'
    m = re.search(bt, text, flags=re.IGNORECASE)
    if m is not None:
        print(m.group())
        print("match success")
        return 'Y'
    else:
        return 'N'

# 微信提醒
def wechatNotify(msg):
    # itchat.auto_login(hotReload=True)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 重要信息，谁发的，在哪个群，时间
    # TODO: 以后看能否提出换汇数量和换汇方式等等
    itchat.send("%s, 有业务了! From: %s, 群: %s, Content: %s" % (nowTime, msg.ActualNickName, msg.User.NickName ,msg.text), toUserName='filehelper')


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if stringMatch(msg.text) == 'Y':
        wechatNotify(msg)



itchat.auto_login(hotReload=True)
itchat.run(True)