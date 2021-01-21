from hashlib import sha512
from src.Core.utils import emailSender,GmailSender,objectIDtoStr,encodeToken,decodeToken,encodeBooks
from hashlib import sha256
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
                'transaction':[]
            }
            col=db['users']
            x=col.insert_one(activeUser)
            _ret=encodeToken({"_id":str(x.inserted_id),'username':basicInfo['username']})
            return({"usertoken":_ret})
        else:
            return 'hash is wrong'
def buyNewBook(data,db):
    try:username=decodeToken(data['token'])
    except Exception as e:return 'wrong token'
    if(data):
        col=db['dispayments']
        # print(data)
        # return 'maintence'
        buys=[]
        for n in data['buys']:
            books=db['users'].find_one({'username':n['owner']['username']})['books']
            for i in books:
                if(i['hash']==n['hash']):
                    n['url']=i['url']
                    continue
            buys.append(n)
        print(buys)
        orderId=sha256(bytes(str(data).encode('utf8'))).hexdigest()
        col.insert_one({
            "order_id":orderId,
            'buys':buys,
            'status':0,
            "buyer":username['username'],
            
        })
        return orderId
    else:
        return 'empty ordering'
def updateOrdersBook(data,db):
    if('status' and 'hash' in data):
        bookToBuy=db['dispayments'].find_one({'order_id':data['hash']})
        
        if(bookToBuy!=None and data['status']==1):
            _ret=[]
            for i in bookToBuy['buys']:
                userInfo=db['users'].find_one({"username":i['owner']['username']})
                transactions=userInfo['transaction']
                transactions.append({
                    "name":i['name'],
                    "price":i['price'],
                    "hash":i["hash"],
                    "status":"unpaid",
                    "pic":i['pic'],
                    "url":i['url']
                })
                
                userInfo['transaction']=transactions
                db['users'].update_one({"username":i['owner']['username']},{"$set":userInfo})
                buyerInfo=db['users'].find_one({"username":bookToBuy['buyer']})
                buyerTransaction=buyerInfo['transaction']
                buyerTransaction.append({
                    "name":i['name'],
                    "price":i['price'],
                    "hash":i['hash'],
                    "pic":i['pic'],
                    "url":i['url']
                })
                buyerInfo['transaction']=buyerTransaction
                print(buyerInfo)
                db['users'].update_one({"username":bookToBuy['buyer']},{"$set":buyerInfo})
            return 'maintence'
def cashout(data,db):
    try:username=decodeToken(data['token'])
    except Exception as e:return 'wrong token'
    userInfo=db['users'].find_one(username)
    if(userInfo):
        userInfo.update({'cashout':True})
        print(userInfo)
        db['users'].update_one({"username":username['username']},{"$set":userInfo})
        return objectIDtoStr(db['users'].find_one({"username":username['username']}))
        