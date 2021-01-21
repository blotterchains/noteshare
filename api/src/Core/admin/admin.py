from src.Core.utils import *

def deleteBook(data,db):
    userInfo=db['users'].find_one({"username":data['owner']['username']})
    books=userInfo['books']
    counter=0
    for i in books:
        if(i['hash']==data['hash']):
            
            books.pop(counter)
        else:
            counter+=1
            continue
    userInfo['books']=books
    db['users'].update_one({"username":data['owner']['username']},{"$set":userInfo})
    db['books'].delete_one({"hash":data['hash']})
    return db['users'].find_one({"username":data['owner']['username']})['books']
def allcashout(data,db):
    findcash=db['users'].find({"cashout":True},{
        "transaction.pic":1,
        "transaction.name":1,
        "transaction.status":"unpaid",
        "transaction.price":1,
        "username":1})
    allcashouts=[]
    for i in findcash:
        allcashouts.append(objectIDtoStr(i))
    
    return allcashouts
def payCashout(data,db):
    userinfo=db['users'].find_one({"username":data['username']})
    buys=[]
    tt=None
    for i in filter(deleteArraywith,userinfo['transaction']):
        buys.append(i)
    userinfo["cashout"]=False
    userinfo['transaction']=buys
    db['users'].update_one({'username':data['username']},{"$set":userinfo})
    info=db['users'].find_one({'username':data['username']})
    return objectIDtoStr(info)