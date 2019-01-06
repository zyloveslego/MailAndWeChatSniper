# -*- coding: UTF-8 -*-
import itchat
from itchat.content import *

import re
import datetime

# version1.0 如果群收到的消息里，有想要的信息，则在filehelper里提醒
"""
msg.actualNickName    user name who send the message
msg.text              content of the message
msg.User.NickName     group name(if it is in group chat)

"""



# 搜索字符串
def stringMatch(text):
    bt = 'rmb|人民币|dollar|美元|美金'
    m = re.search(bt, text, flags=re.IGNORECASE)
    if m:
        print(m.group())
        print("match success")
        return True
    else:
        return False
    
# 微信提醒
def wechatNotify(msg):
    # itchat.auto_login(hotReload=True)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 重要信息，谁发的，在哪个群，时间
    # TODO: 以后看能否提出换汇数量和换汇方式等
    # print the time, user name(备注名 in group chat), group name, message content
    itchat.send("%s, 有业务了! From: %s, 群: %s, Content: %s" % (nowTime, msg.ActualNickName, msg.User.NickName ,msg.text), toUserName='filehelper')


# Override the messages in the group chat.(处理群消息)
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    # if I am been @, then repley the message.
    if msg.isAt:
        #msg.user.send(u'@%s\u2005 I received: %s' % (
        #msg.user.send('@%s I received: %s' % (
            #msg.actualNickName, msg.text))
        msg.user.send("@%s 不好意思，强仔正在搞项目。请问有什么事需要找他呢？可以方便告诉我，然后我转告给他吗？～～" % msg.actualNickName)
    if stringMatch(msg.text):
        wechatNotify(msg)


# copy what you said in personal chat into your account(将你在单人聊天里的话都copy到自己的号里)
# 同时也是用于自动回复
@itchat.msg_register(TEXT)
def _(msg):
    # equals to print(msg['FromUserName'])
    print(msg.fromUserName)   # print long id
    if '作者' in msg['Text'] or '主人' in msg['Text']:
        return '你可以在这里了解他：https://github.com/littlecodersh'
    elif '源代码' in msg['Text'] or '获取文件' in msg['Text']:
        itchat.send('@fil@main.py', msg['FromUserName'])
        return u'这就是现在机器人后台的代码，是不是很简单呢？'
    elif u'获取图片' in msg['Text']:
        itchat.send('@img@applaud.gif', msg['FromUserName']) # there should be a picture
    else:
        return "不好意思，强仔正在搞项目。请问有什么事需要找他呢？可以方便告诉我，然后我转告给他吗？～～ "


# check what type of message that we received.
@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def atta_reply(msg):
    return ({ 'Picture': u'图片', 'Recording': u'录音',
        'Attachment': u'附件', 'Video': u'视频', }.get(msg['Type']) +
        u'已下载到本地')


@itchat.msg_register(['Map', 'Card', 'Note', 'Sharing'])
def mm_reply(msg):
    if msg['Type'] == 'Map':
        return u'收到位置分享'
    elif msg['Type'] == 'Sharing':
        return u'收到分享' + msg['Text']
    elif msg['Type'] == 'Note':
        return u'收到：' + msg['Text']
    elif msg['Type'] == 'Card':
        return u'收到好友信息：' + msg['Text']['Alias'] 


@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('Nice to meet you!')

#可以多开一个聊天机器人， 是否可以无限多开？
newInstance = itchat.new_instance()
newInstance.auto_login(hotReload=True, statusStorageDir='newInstance.pkl')
newInstance.run()

#登陆的时候使用命令行显示二维码, 程序关闭，一定时间内重新开启也可以不用重新扫码
itchat.auto_login(hotReload=True)
itchat.run(True)

