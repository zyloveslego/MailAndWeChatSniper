import itchat
from itchat.content import *

import re
import datetime

import MySQLdb

import json

# 设置字符串匹配字符串
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
def wechatNotify(msg, forwardGroups, keywordList):

    """
    id
    User
    Listener
    Forward
    KeyWord

    收到群消息，匹配Listener字段
    然后匹配Keyword，Keyword存储方式为a|b|c|d
    匹配成功则转发给Forward中的群
    """

    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        # 默认发送给文件传输助手
        print("forwarding")

        itchat.send("%s, 有业务了! 发消息人: %s, 来自群: %s, 内容: %s" % (nowTime, msg.ActualNickName, msg.User.NickName, msg.text), toUserName='filehelper')
        # 转发的时候需要匹配msg.User.UserName，不能使用NickName
        # 转发给设置需要转发的群
        for forwardGroup, keywordSend in zip(forwardGroups, keywordList):
            forwardGroupInfo = itchat.search_chatrooms(name=forwardGroup)
            forwardGroupUserName = forwardGroupInfo[0]['UserName']
            itchat.send("%s。关键字: %s。来自群: %s, 内容: %s" % (nowTime, keywordSend, msg.User.NickName, msg.text), forwardGroupUserName)

        print("forward success")
    except Exception as e:
        print(e)




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

    cursor = db.cursor()
    # 如果收到的Listener的消息
    sql = "SELECT * FROM wechatRule WHERE Listener = '" + msgFromGroupNickName + "'"

    try:
        # 执行sql语句
        cursor.execute(sql)

        # 找出所有Listener是该群的群
        forwardGroups = []
        keywordList = []
        keyword = None

        results = cursor.fetchall()

        for row in results:
            User = row[1]
            Listener = row[2]
            Forward = row[3]
            KeyWord = row[4]

            # print(User)
            # print(Listener)
            # print(Forward)
            # print(KeyWord)

            # 如果字符串匹配
            keyword = stringMatch(msg.text, KeyWord)
            if keyword:
                forwardGroups.append(Forward)
                keywordList.append(keyword)

            keyword = None

        print(keywordList)
        print(forwardGroups)
        # 需要转发的群以及关键字
        if keywordList != []:
            wechatNotify(msg, forwardGroups, keywordList)

        db.commit()




    except:
        # 发生错误时回滚
        db.rollback()



if __name__ == '__main__':
    # 相关值初始化，以后改为客户输入，是否需要自动联想
    # TODO: 数组库存转发规则
    # 搜索的字符串暂定用|隔开
    # searchString = ''
    # # 监听群
    # listenerGroups = ''
    # # 转发群
    # forwardGroups = ''
    # # 转发附加信息，可选
    # forwardMsg = ''

    # 打开数据库连接
    # TODO: 上传时记得删密码
    db = MySQLdb.connect("localhost", "", "", "wechat", charset='utf8')


    #登陆的时候使用命令行显示二维码, 程序关闭，一定时间内重新开启也可以不用重新扫码
    itchat.auto_login(hotReload=True)
    itchat.run()

    print("over")
    db.close()
