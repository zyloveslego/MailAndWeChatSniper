import itchat
from itchat.content import *

import re
import datetime

import MySQLdb



# 设置字符串匹配字符串
def stringMatch(text, searchString):
    """

    :param text: input text
    :param searchString: match string
    :return: a list of matched string
    """

    # searchString = 'rmb|人民币|dollar|美元|美金'
    matchedString = re.findall(searchString, text, flags=re.IGNORECASE)
    if matchedString:
        print(matchedString)
        print("match success")
        return matchedString
    else:
        return False


# 微信提醒
def wechatNotify(msg, forwardList, keywordList):
    """

    :param msg: wechat msg
    :param forwardList: forward group list
    :param keywordList: keyword list for each forward group
    :return: None
    """

    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        # 默认发送给文件传输助手
        print("forwarding")

        itchat.send("%s, 有业务了! 发消息人: %s, 来自群: %s, 内容: %s" % (nowTime, msg.ActualNickName, msg.User.NickName, msg.text), toUserName='filehelper')
        # 转发的时候需要匹配msg.User.UserName，不能使用NickName
        # 转发给设置需要转发的群
        for forwardGroup, keywordSend in zip(forwardList, keywordList):
            # forwardGroupInfo = itchat.search_chatrooms(name=forwardGroup)
            # forwardGroupUserName = forwardGroupInfo[0]['UserName']
            itchat.send("%s。关键字: %s。来自群: %s, 内容: %s" % (nowTime, keywordSend, msg.User.NickName, msg.text), forwardGroup)

        print("forward success")
    except Exception as e:
        print(e)




# Override the messages in the group chat.(处理群消息)
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    """
    1. 收到群消息
    2. 首先判断是来自哪个群
    3. 然后确定需要转发给哪些群
    4. 判断是否有关键字
    5. 逐个转发

    """

    msgFromGroupUserName = msg.User.UserName
    print("msg receive from " + msgFromGroupUserName)
    # TODO: 突然出现了msg中没有NickName的情况
    print(msg.User.NickName)

    cursor = db.cursor()
    # 如果收到的Listener的消息
    # sql = "SELECT * FROM wechatRule WHERE Listener = '" + msgFromGroupNickName + "'"
    sql = "SELECT * FROM ForwardRule WHERE ListenerID = '" + msgFromGroupUserName + "'"


    try:
        # 执行sql语句
        cursor.execute(sql)

        # 找出所有ListenerID是该群的群
        forwardList = []
        keywordList = []
        matchedString = None

        results = cursor.fetchall()

        for row in results:
            UserID = row[1]
            ListenerID = row[2]
            ForwardID = row[3]
            KeyWord = row[4]


            # 如果字符串匹配
            matchedString = stringMatch(msg.text, KeyWord)

            if matchedString:
                # 将需要转发的对象和关键字存入forwardLists和keywordList两个list
                if ForwardID:
                    forwardList.append(ForwardID)
                else:
                    forwardList.append(UserID)

                keywordList.append(matchedString)

            matchedString = None

        print(keywordList)
        print(forwardList)

        # 需要转发的群以及关键字
        if keywordList != []:
            wechatNotify(msg, forwardList, keywordList)

        db.commit()




    except:
        # 发生错误时回滚
        db.rollback()



if __name__ == '__main__':
    # 搜索的字符串暂定用|隔开

    # 数据库连接
    # TODO: 上传时记得删密码
    db = MySQLdb.connect("localhost", "", "", "wechatForwardDB", charset='utf8')


    #登陆的时候使用命令行显示二维码, 程序关闭，一定时间内重新开启也可以不用重新扫码
    itchat.auto_login(hotReload=True)
    itchat.run()

    print("over")
    db.close()
