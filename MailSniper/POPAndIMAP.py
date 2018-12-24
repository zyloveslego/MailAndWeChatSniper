# -*- coding: UTF-8 -*-
# !--------------!
# gmail需要打开pop和IMAP，并且允许不安全的应用访问

# pop下载后就从pop服务器删除了，所以只会读取一次

# IMAP会存所有收到的邮件，需要代码设置为seen

import time
import re

import poplib
import email, sys
from imapclient import IMAPClient, SEEN

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


# POP
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            # 这里+8是什么意思
            charset = content_type[pos + 8:].strip()
    return charset

def print_info(msg, indent=0):
    if indent == 0:
        # 邮件的From, To, Subject存在于根对象上
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        # 如果邮件对象是一个MIMEMultipart
        # get_payload()包含所有的子对象
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        # 邮件对象不是一个MIMEMultipart
        content_type = msg.get_content_type()
        # 文本
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
        # 非文本
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))


def getMailContentbyPOP(mail, password, pop3_server):
    server = poplib.POP3_SSL(pop3_server)
    try:
        print("connecting")
        # server.set_debuglevel(1)
        server.user(mail)
        server.pass_(password)
        print("success connect")

        # stat()返回邮件数量和占用空间:
        message, size = server.stat()
        # print('Messages: %s. Size: %s' % (message, size))

        if message != 0:
            # list()返回所有邮件的编号:
            resp, mails, octets = server.list()

            # 获取最新一封邮件, 注意索引号从1开始:
            index = len(mails)
            # print(index)
            for i in range(index):
                resp_first, lines, octets_first = server.retr(i + 1)

                # Message对象本身可能是一个MIMEMultipart对象，即包含嵌套的其他MIMEBase对象，嵌套可能还不止一层
                msg_content = b'\r\n'.join(lines).decode('utf-8')
                msg = Parser().parsestr(msg_content)

                try:
                    # print_info(msg)
                    if stringMatch(str(msg)) == 'Y':
                        # TODO: 如果msg中有相关信息则通知
                        print("有业务了")
                except Exception as e:
                    print(e)
        else:
            print("No new mail")

    except:
        print("success failed")

    finally:
        server.quit()


# IMAP
def getMailContentbyIMAP(mail, password, imap_server):
    conn = IMAPClient(imap_server, ssl=True)
    try:
        conn.login(mail, password)
        print("success connect")
    except conn.Error:
        print('Could not log in')
        sys.exit(1)
    else:
        conn.select_folder('INBOX', readonly=False)
        # 利用select_folder()函数选择文件夹，'INBOX'为收件箱

        result = conn.search('UNSEEN')
        conn.add_flags(result, [SEEN])
        msgdict = conn.fetch(result, ['BODY.PEEK[]'])

        # 现在已经把邮件取出来了，下面开始解析邮件
        for message_id, message in msgdict.items():
            e = email.message_from_bytes(message[b'BODY[]'])  # 生成Message类型

            # 由于'From', 'Subject' header有可能有中文，必须把它转化为中文
            subject = email.header.make_header(email.header.decode_header(e['SUBJECT']))
            mail_from = email.header.make_header(email.header.decode_header(e['From']))

            # 解析邮件正文
            maintype = e.get_content_maintype()
            if maintype == 'multipart':
                for part in e.get_payload():
                    if part.get_content_maintype() == 'text':
                        mail_content = part.get_payload(decode=True).strip()
            elif maintype == 'text':
                mail_content = e.get_payload(decode=True).strip()

            # content转化成中文
            try:
                if mail_content != None:
                    mail_content = mail_content.decode('gbk')
            except UnicodeDecodeError:
                print('decode error')

            else:
                # print('new message')
                # print('From: ', mail_from)
                # print('Subject: ', subject)
                # print('-' * 10, 'mail content', '-' * 10)
                # print(mail_content.replace('<br>', '\n'))
                # print('-' * 10, 'mail content', '-' * 10)
                if stringMatch(str(subject)) == 'Y' or stringMatch(str(mail_content)) == 'Y':
                    # TODO: 如果msg中有相关信息则通知
                    print("有业务了")
    finally:
        conn.logout()



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



if __name__ == "__main__":
    mail = ""
    password = ""
    pop3_server = "pop.gmail.com"
    imap_server = 'imap.gmail.com'

    while(1):
        # pop和imap选一种
        # getMailContentbyPOP(mail, password, pop3_server)
        getMailContentbyIMAP(mail, password, imap_server)
        print("sleep 60s")
        time.sleep(60)