# -*- coding: utf-8 -*- 
import requests
import smtplib
import email.message
import jwt
from bson import ObjectId
from hashlib import sha256
def encodeBooks(data):
    plantext=bytes(str(data).encode('utf8'))
    return sha256(plantext).hexdigest()
def encodeToken(data):
    try:

        return jwt.encode(data,'notsosecurepassword',algorithm='HS256')
    except Exception as e:
        print(e)
def decodeToken(data):
    decoded=jwt.decode(bytes(data.encode('utf8')),'notsosecurepassword',algorithms='HS256')
    decoded['_id']=ObjectId(decoded['_id'])
    return decoded
def isIntType(data):
    types=[
        '_id',
        'price',
        'balance',

    ]
    if(data in types):
        return True
    else:
        return False
def objectIDtoStr(data):
    data['_id']=str(data['_id'])
    
def emailSender(msg,sub,to):
    data={"from": "wizif <mailgun@sandbox2d873de64b4546b8b375b7e1d0f9b33f.mailgun.org>",
			"to": "{}".format(to),
			"subject": "{}".format(sub),
			"text": "{}".format(msg)}
    print(data)
    return requests.post(
		"https://api.mailgun.net/v3/sandbox2d873de64b4546b8b375b7e1d0f9b33f.mailgun.org/messages",
		auth=("api", "126ea4882eb4da2d7c4c6e0c9b86fc88-b6190e87-5b1d977c"),
		data={
            "from": "wizif <mailgun@sandbox2d873de64b4546b8b375b7e1d0f9b33f.mailgun.org>",
			"to": "{}".format(to),
			"subject": "{}".format(sub),
			"text": "sss"
            }

    )
def GmailSender(body,sub,to):
    
    server = smtplib.SMTP('smtp.gmail.com:587')
    email_content = body
    msg = email.message.Message()
    msg['Subject'] = sub
    msg['From'] = 'noteshare2021@gmail.com'
    password = "Ut2U=z9pY$YN7DB7"   
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_content)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], to, msg.as_string())            
def isPublic(data):
    collections=[
        'books'        
    ]
    if(data in collections):
        return True
    else:
        return False
