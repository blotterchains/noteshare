from hashlib import sha512
from src.Core.utils import emailSender,GmailSender,objectIDtoStr,encodeToken,decodeToken,encodeBooks
def login(data,db):
    if('username' and 'password' in data):
        col=db['users']
        myquery={'password':data['password'],'username':data['username']}
        x=col.find_one(myquery)
        if(x==None):
            return 'username or password is incorrect'
        else:
            objectIDtoStr(x)     
            _ret={
                'usertoken':encodeToken({"_id":str(x['_id']),'username':x['username']})
            }

            return(_ret)
    else:
        return 'enter username and password'
def getUserInfo(data,db):
    if('token' in data):
        try:query=decodeToken(data['token'])
        except Exception as e:return 'wrong token'
        col=db['users']
        _ret=col.find_one(query)
        if(_ret!=None):
            objectIDtoStr(_ret)
            print(_ret)
            return _ret
        else:
            return 'expired token'

def signup(data,db):
    if('username' and 'password' and 'email' in data):
        col= db['disusers']
        userhash=data
        for i in range(0,5):
            userhash= sha512(('%s'%userhash).encode('utf8')).hexdigest()
        
        data.update({'active':userhash})
        x=col.insert_one(data)
        msg="""
        active your account
        http://localhost:3000/%s/active
        """%(userhash)
        to=data['email']
        sub='active noteshare account'
        GmailSender(msg,sub,to)
        return 'registered'
    else:
        return 'plz enter all fields'
def compeleteSignUp(data,db):
    if('hash' in data):
        col=db['disusers']
        basicInfo=col.find_one({'active':data['hash']})
        print(basicInfo)
        if(basicInfo!=None):
            objectIDtoStr(basicInfo)
            # basicInfo['_id']=str(basicInfo['_id'])
            activeUser={
                'username':basicInfo['username'],
                'password':basicInfo['password'],
                'books':[],
                'balance':0,
                'profilepic':'',
                'email':basicInfo['email'],
                'trasaction':[]
            }
            col=db['users']
            x=col.insert_one(activeUser)
            _ret=encodeToken({"_id":str(x.inserted_id),'username':basicInfo['username']})
            return({"usertoken":_ret})
        else:
            return 'hash is wrong'