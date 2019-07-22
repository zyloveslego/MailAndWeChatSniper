import itchat
from itchat.content import *

import re
import datetime

import json

# 设置字符串匹配字符串
# TODO: 暴露3个接口，1.匹配的字符串 2.转发和需要转发的群名称 3.回复的内容
def stringMatch(text, searchString):
    # searchString = 'rmb|人民币|dollar|美元|美金'
    m = re.search(searchString, text, flags=re.IGNORECASE)
    if m:
        print(m.group())
        print("match success")
        return m.group()
    else:
        return False

# 微信提醒
# TODO: 可以手动设置监听的群和需要转发的群
def wechatNotify(msg, keyword):
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        # 默认发送给文件传输助手
        print("forwarding")

        itchat.send("%s, 有业务了! 发消息人: %s, 来自群: %s, 内容: %s" % (nowTime, msg.ActualNickName, msg.User.NickName, msg.text), toUserName='filehelper')
        # 转发的时候需要匹配msg.User.UserName，不能使用NickName
        # 转发给设置需要转发的群
        for forwardGroup in forwardGroups:
            forwardGroupInfo = itchat.search_chatrooms(name=forwardGroup)
            forwardGroupUserName = forwardGroupInfo[0]['UserName']
            itchat.send("%s。关键字: %s。来自群: %s, 内容: %s" % (nowTime, keyword, msg.User.NickName, msg.text), forwardGroupUserName)

        print("forward success")
    except:
        pass

# Override the messages in the group chat.(处理群消息)
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):

    # 1. 收到群消息
    # 2. 首先判断是来自哪个群
    # 3. 然后确定需要转发给哪些群
    # 4. 判断是否有关键字
    # 5. 逐个转发

    msgFromGroupNickName = msg.User.NickName
    print("msg receive from " + msgFromGroupNickName)


    # 如果和监听的群名匹配
    if msgFromGroupNickName in listenerGroups:
        # 如果包含必要的信息
        keyword = stringMatch(msg.text, searchString)
        if keyword:
            wechatNotify(msg, keyword)


if __name__ == '__main__':
    # 相关值初始化，以后改为客户输入，是否需要自动联想
    # TODO: 客户的输入方式
    # 搜索的字符串暂定用|隔开
    searchString = 'rmb|人民币|dollar|美元|美金|123'
    # 剩下的选项用list
    # 监听群
    listenerGroups = ['XM机器人官方董事会🐼']
    # 转发群
    forwardGroups = ['XM机器人官方董事会🐼', '测试群2号']
    # 转发附加信息，可选
    forwardMsg = []


    #登陆的时候使用命令行显示二维码, 程序关闭，一定时间内重新开启也可以不用重新扫码
    itchat.auto_login(hotReload=True)
    itchat.run()
