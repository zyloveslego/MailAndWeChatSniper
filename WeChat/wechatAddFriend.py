# -*- coding: UTF-8 -*-
import itchat
from itchat.content import *

@itchat.msg_register(TEXT, isGroupChat=True)
def wechatNotify(msg):
    # try:
        # 群信息
        # print(msg.User)
        # 发消息人名称
        print(msg.ActualNickName)
        # 发消息人id
        print(msg.ActualUserName)
        # print(msg.UserName)
        # 群名称
        # print(msg.User.NickName)
        # 群id
        # print(msg.FromUserName)
        # 通过群id找到群中所有人
        detailedChatroom = itchat.update_chatroom(msg.FromUserName, detailedMember=True)
        print(detailedChatroom)

        # 这里的userName是个info dict
        # 通过群聊来获得
        userDict = {}
        for member in detailedChatroom.MemberList:
            # print(member)
            if msg.ActualUserName == member.UserName:
                userDict = member
                break


        # 用id或者info dict都无效
        print(userDict)
        print(itchat.add_friend(userName=userDict, status=2))

    # except:
    #     pass




itchat.auto_login(hotReload=True)
itchat.run(True)