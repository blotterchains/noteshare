from src.Core.utils import *
from time import localtime
def newBook(data,db):
    try:query=decodeToken(data['token'])
    except Exception as e:return 'wrong token'
    col=db['users']
    userInfo=col.find_one(query)
    books=userInfo['books']
    insertInfoIntoUser={
        "author": data["author"],
        "description": data["description"],
        "hash":  encodeBooks({'_id':query['_id'],'name':data['name']}),
        "littledesc": data["littledesc"],
        "name": data["name"],
        "owner": {
            "_id": str(query['_id']),
            "username": query['username']
        },
        "pages": data['pages'],
        "pic": data['images'][0],
        "price": data['price'],
        "rank": "1",
        "type": data['type'],
        "url": data['url'],
        "buyers":[],
        "comments":[],
        "images":data['images']
    }
    
    insertInfoIntoBooks= {
        "author": data["author"],
        "description": data["description"],
        "hash":  encodeBooks({'_id':query['_id'],'name':data['name']}),
        "littledesc": data["littledesc"],
        "name": data["name"],
        "owner": {
            "_id": str(query['_id']),
            "username": query['username']
        },
        "pages": data['pages'],
        "pic": data['images'][0],
        "price": data['price'],
        "rank": "1",
        "type": data['type'],
        "url": data['url']
    }
    db['books'].insert_one(insertInfoIntoBooks)
    books.append(insertInfoIntoUser)
    newvalues = { "$set": {'books':books} }
    col.update_one(query,newvalues)
    userInfo=col.find_one(query)
    objectIDtoStr(userInfo)
    return userInfo
def updateBook(data,db):
    try:query=decodeToken(data.pop('token'))
    except Exception as e:return 'wrong token'
    col=db['users']
    userInfo=col.find_one(query)
    books=userInfo['books']
    cc=0
    for i in books:
        if(i['hash']==data['hash']):
           
            books[cc]=data
            
            bookIntoBooks=data
            break
        else:
            cc+=1
            continue
    userInfo['books']=books
    col.update_one(query,{"$set":userInfo})
    bookIntoBooks.pop('comments')
    bookIntoBooks.pop('buyers')
    bookIntoBooks.pop('images')
    updatequery={'hash':data['hash']}
    db['books'].update_one(updatequery,{"$set":bookIntoBooks})    
    _ret=col.find_one(query)
    _ret.pop('_id')
    return _ret
def getBookInfo(data,db):
    col=db['users']
    userInfo=col.find_one({"username":data['username']})
    books=userInfo['books']
    _ret={}
    for i in books:
        if(i['hash']==data['hash']):
            _ret=i
            break
        else:
            continue
    if(_ret['price']!='free'):
        _ret['url']=''
    else:
        pass
    return (_ret)
def insertComment(data,db):
    if('text' and 'hash' and 'token' and 'username'):
        try:senderUserInfo=decodeToken(data['token'])
        except Exception as e:return str(e)
        print(data)
        col=db['users']
        userInfo=col.find_one({'username':data['username']})
        
        books=userInfo['books']
        for i in books:
            if(i['hash']==data['hash']):
                comments=i['comments']
                currentDate="%s/%s/%s"%(localtime().tm_year,localtime().tm_mon,localtime().tm_mday)
                i['comments'].append({
                    'date':currentDate,
                    'text':data['text'],
                    'username':senderUserInfo['username']
                })
                break
            else:
                continue
        userInfo['books']=books
        col.update_one({'username':data['username']},{"$set":userInfo})
        _ret=col.find_one({'username':data['username']})
        _ret.pop('_id')
        return _ret
    else:
        return 'wrong inputs'