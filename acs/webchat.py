import requests
from bs4 import BeautifulSoup
import re
import json
import sqlite3,os

# Get encrypted response text

httpurl=os.getenv("HOST")

deptid=os.getenv("deptid")

print(httpurl)

#httpurl="47.99.229.124:1027"

api = 'https://mp.weixin.qq.com/mp/audio?scene=105&__biz=MjM5NjAxOTU4MA==&mid=3009222479&idx=2&voice_id=MjM5NjAxOTU4MF8zMDA5MjIyNDc4&sn=ca6dff2422766bbc8a09015229681ea6#wechat_redirect'

response = requests.post(api)

ctx=response.content

soup = BeautifulSoup(ctx,'html.parser')

v=soup.find("body").find_all("script")[11]

script = v.get_text("|", strip=True)

#print(script)

pattern = re.compile(r'title : ".*"')
title=pattern.findall(script)

pattern = re.compile(r'voiceid : ".*"')
voice=pattern.findall(script)

to=(title[0].replace("title :","").strip())
vo=(voice[1].replace("voiceid :","").replace('"',"").strip())


conn = sqlite3.connect('/tmp/msg.db')

c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS indexmsg
       (ID INTEGER PRIMARY KEY   autoincrement,
       NAME           TEXT    NOT NULL,
       VO            TEXT     NOT NULL);''')

conn.commit()

cursor = c.execute("SELECT count(1) from indexmsg where VO='%s'"%vo)

res = cursor.fetchone()


headers = \
    {
        "apptype": "BCP",
        "Content-Type": "application/json;charset=UTF-8"
    }


if(res[0]==0):

    midurl="https://res.wx.qq.com/voice/getvoice?mediaid=%s"%vo

    #rs_url="http://www.mbos.com/"
    rs_url="http://%s/mbos/ding_media_ctrl/upload"%httpurl

    rsdata={"corpId":"ding62aaa29d6c83d2e1","mediaUrl":midurl,"mediaName":to,"mediaType":"voice","duration":60}

    rsjson=(json.dumps(rsdata, ensure_ascii=False))

    #print(rsjson)

    response = requests.post(rs_url, headers=headers,data=rsjson.encode("utf8"),timeout=5).text

    content=json.loads(response)
    print(content["code"])
    print(content["data"]["mediaId"])

    mediaid=content["data"]["mediaId"]

    msgtxt_url = "http://%s/mbos/ding_msg_ctrl/send_text_msg"%httpurl

    msgvo_url = "http://%s/mbos/ding_msg_ctrl/send_voice_msg"%httpurl


    #msgdata = {"mediaId":mediaid,"content":to,"title":to,"msgType":"text","deptId":"57284272","sender":"pyinfomation","corpId": "ding62aaa29d6c83d2e1","duration":60}

    msgdata = {"mediaId": mediaid, "content": to, "title": to, "msgType": "text", "deptId": deptid,
               "sender": "pyinfomation", "corpId": "ding62aaa29d6c83d2e1", "duration": 60}

    rsjson = (json.dumps(msgdata, ensure_ascii=False))

    #print(rsjson)

    response = requests.post(msgtxt_url, headers=headers, data=rsjson.encode("utf8"), timeout=5).text

    content = json.loads(response)


    response = requests.post(msgvo_url, headers=headers, data=rsjson.encode("utf8"), timeout=5).text

    content = json.loads(response)

    if(content["code"]==0):
        c.execute('insert into indexmsg(NAME,VO) VALUES  (?,?)',(to,vo))
        conn.commit()
else:
    print("msg allready send!")


