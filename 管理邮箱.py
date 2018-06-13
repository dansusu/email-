#poplib负责从  MDA  到  MUA
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

#下载并解析
def getMsg():
    email="1336678869@qq.com"
    pwd="jibugaosuni"
    #pop3服务地址
    pop3_srv="pop.qq.com"
    #安全通道
    srv = poplib.POP3_SSL(pop3_srv)
    #绑定账号密码
    srv.user(email)
    srv.pass_(pwd)
    #stat返回邮件数量和占用空间
    msgs,count=srv.stat()
    print("Message:{0}，Size:{1}".format(msgs,count))
    rsp.mails,octets = srv.list()
    print(mails)
    index = len(mails)
    #retr负责返回带有索引的一封信的内容
    rsp,lines,octets =srv.retr(index)
    #获得原始文本
    msg_count=b'\r\n'.join(lines).decode("utf-8")
    #解析
    msg=Parser().parsestr(msg_count)
    #关闭连接
    srv.close()
    return msg

def parseMsg(msg, indent=0):
    if indent==0:
        for header  in ['From','To','Subject']:
            value=msg.get(header,'')
            if value:
                if header=='Subject':
                    value=decodeStr(value)
                else :
                    hdr,addr=parseaddr(value)
                    name=decodeStr(hdr)
                    value="{0}<{1}>".format(name,addr)
            print("{0}，{1}：{2}".format(indent,header,value))
    #邮件本身
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n,part in enumerate(parts):
            print("{0}spart:{1}".format(' '*indent,n))
            parseMsg(part,indent+1)
    else:
        #get_content_type是系统提供的函数，得到内容类型
        content_type=msg.get_content_type()
        if (content_type=='text/plain' or content_type=='text/html'):
            content=msg.get_payload(decode=True)
            charset=guessCharset(msg)
            if charset:
                content=content.decode(charset)
            print("{0}Text:{1}".format(indent,content))

        else:
            print("{0}Attrachment:{1}".format(indent,content_type))

def decodeStr(s):
    #s解码，解码是编码的逆过程
    value,charset=decode_header(s)[0]
    if charset:
        value=value.decode(charset)
    return value

def guessCharset(msg):
    #猜测邮件编吗格式
    charset=msg.get_charset()

    if charset is  None:
        content_type=msg.get("Content-Type","").lower()
        pos=content_type.find("charset=")
        if pos >= 0:
            charset = content_type[pos+8:].strip()
    return charset

if __name__=='__main__':
    msg=getMsg()
    print(msg)
    parseMsg(msg,0)









