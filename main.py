import sys
import os
from urllib import response
from models import Anuncio
import pymongo

from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# uri = 'mongodb+srv://canal:canal@cluster0.vodgj.mongodb.net/appsNube?retryWrites=true&w=majority'

# uri = os.environ['MONGODB_URI'] + '?ssl_cert_reqs=CERT_NONE' 
uri = 'mongodb+srv://fran:fran12@cluster0.zfsyd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true'
client = pymongo.MongoClient(uri)

db = client.get_default_database()  

Anuncios = db['Anuncios']

# Definicion de metodos para endpoints

@app.route('/Anuncio', methods=['GET'])
def showAds():
    
    # return render_template('ads.html', ads = list(ads.find().sort('date',pymongo.DESCENDING)))
    r = list(Anuncios.find())
    if (request.args.get('nombre') != None):
        r2 = r
        r = []
        for a in r2:
            if a['nombre'] == request.args.get('nombre'):
                r.append(a)
    return str(r)
    
@app.route('/Anuncio', methods = ['POST'])
def newAd():
    anuncio = Anuncio()
    anuncio.nombre = request.json['nombre']
    anuncio.descripcion = request.json['descripcion']
    anuncio.longitud = request.json['longitud']
    Anuncios.insert_one(anuncio.__dict__)
    return str(list(Anuncios.find()))

@app.route('/Anuncio/<_id>', methods = ['POST'])
def editAd(_id):
    
    anuncio = Anuncio()
    anuncio.nombre = request.json['nombre']
    anuncio.descripcion = request.json['descripcion']
    anuncio.longitud = request.json['longitud']
    Anuncios.update_one({'_id': ObjectId(_id) }, { '$set': anuncio.__dict__ })    
    return str(list(Anuncios.find()))

@app.route('/Anuncio/<_id>', methods = ['DELETE'])
def deleteAd(_id):
    
    Anuncios.delete_one({'_id': ObjectId(_id)})
    return str(list(Anuncios.find()))

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App Engine
    # or Heroku, a webserver process such as Gunicorn will serve the app. In App
    # Engine, this can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
