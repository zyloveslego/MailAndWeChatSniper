# MailAndWeChatSniper

POP和IMAP只用一种即可

gmail需要打开pop和IMAP，并且允许不安全的应用访问

pop下载后就从pop服务器删除了，所以只会读取一次

IMAP会存所有收到的邮件，需要代码设置为seen

微信登录后如果程序断开，过一段时间后可能会需要在手机上点确认按钮来登录



# WeChat version1.0 
如果群收到的消息里，有想要的信息，则在filehelper里提醒


# WeChat version2.0
监听listenerID群，匹配keyWord后，转发给forwardID群

# 数据库

参见DB.md

版本：mysql  Ver 8.0.11 for osx10.13 on x86_64


**GroupInfo** : GroupID, GroupName

**UserInfo** : UserID, UserName

**ForwardRule** : UserID(ref UserInfo.UserID), ListenerID(ref GroupInfo.GroupID), ForwardID(ref GroupInfo.GroupID), keyWord
