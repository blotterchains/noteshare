
from src.Core.utils import  isIntType
import pymongo
def index(data,col):
    x=col.insert_one(data)
    return x.inserted_id
def update(data,col):

    myquery = {"_id":data['_id']}
    # myquery = {"username":data['username']}
    newvalues = { "$set": data }
    col.update_one(myquery,newvalues)
    _ret=[]
    for x in col.find(data):
        _ret.append(x)
    return _ret
def find(data,col):
    if('limit' and 'page' in data):

        limit=int(data.pop('limit'))
        page=int(data.pop('page'))
    else:
        return 'plz enter limit and page'
    dd=data
    for i in data:
        if(isIntType(i)):
            data[i]=int(data[i])
        else:
            data[i]={'$regex': '.*%s.*'%data[i]}
    myquery={
            "$or":[dd]
    }
    _ret=[]
    for x in col.find(myquery).skip(page*limit).limit(limit).sort("_id",-1):
        x['_id']=str(x['_id'])
        try:
            if(x['price']!='free'):
                x['url']=''
        except:pass
        _ret.append(x)
    return _ret
def clear(data,col):
    for x in col.find():
        col.delete_one({"_id":x["_id"]})
        print(x)
    return {"status":"you are updating"}