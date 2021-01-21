from flask import Flask,jsonify,request,render_template
from flask_cors import CORS
import src.Core.routes as routes
import pymongo
from werkzeug.utils import secure_filename
from time import sleep
from random import randint
from base64 import b64decode
from uuid import uuid4
conn=pymongo.MongoClient("mongodb://127.0.0.1:27017")
db=conn['noteshare']
app=Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER']='./uploads'
# TODO: later:
@app.route("/api",methods=["POST"])
def endNode():

    try:

        data=request.get_json()
    except:
        print('hell')
        data={}
    try:

        action=request.headers["action"]
    except:
        return {"status":"no action found"}
    #edit this
    # try:
    #     
    #     # token=request.get_header["Utoken"]
        
    # except:
    #     pass
    # if("action" in action):
    """remeber all functions should get data"""
    print(action.split('-')[0])
    if('update'==action.split('-')[0] or 'find'==action.split('-')[0] or 'clear'==action.split('-')[0]):
        _ret=routes.dispacther()[action.split('-')[0]](data,db[action.split('-')[1]])
    else:
        _ret=routes.dispacther()[action](data,db)
    return jsonify(_ret)
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:

            data=request.get_json()
            filename='./static/'+uuid4().hex
            if('data:application/pdf;base64,' in data['file']):
                try:
                    data['file']=data['file'].replace('data:application/pdf;base64,','')
                    zz=open(filename+'.pdf','wb')
                    zz.write(b64decode(data['file']))
                    return jsonify({'url':'http://localhost:5000/'+filename+'.pdf'})
                except :return jsonify('wrong')
            elif('data:image/jpeg;base64,' in data['file']):
                try:
                    data['file']=data['file'][data['file'].find('/9'):]
                    zz=open(filename+'.jpg','wb')
                    zz.write(b64decode(data['file']))
                    return jsonify({"url":'http://localhost:5000/'+filename+'.jpg'})
                except Exception as e:return jsonify('wrong')
            elif('data:audio/mpeg;base64,' in data['file']):
                try:
                    data['file']=data['file'].replace('data:audio/mpeg;base64,','')
                    zz=open(filename+'.mp3','wb')
                    zz.write(b64decode(data['file']))
                    return jsonify({'url':'http://localhost:5000/'+filename+'.mp3'})
                except :return jsonify('wrong')
            else:return jsonify('wrong type')
        except Exception as e:
            return str(e)
@app.route('/dargah/<hash>')
def dargah(hash):
    return render_template('payment.html',hash=hash)
app.run(debug=True)

        