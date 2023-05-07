import json
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from pymongo import MongoClient
from bson import ObjectId, json_util
client = MongoClient('mongodb://localhost:27017/')
mongo = client.ProyectoCBD

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    recetas = mongo.A.aggregate([{'$project':{
        'receta' : '$receta',
        'ingredientes' : '$ingredientes',
        'tags' : '$tags',
        'autor_info' : '$autor_info'
    }}])
    response = json_util.dumps(recetas)
    response = json.loads(response)
    return render_template("index.html", name = "Javi", recetas = response)


@views.route("/search")
def filter():
    data = request.args
    if(data.get("receta") != ""):
        recetas = mongo.A.aggregate([{
            '$match': {
                'receta' : {'$regex':data.get("receta")}
            }
        },
                                     {'$project':{
        'receta' : '$receta',
        'ingredientes' : '$ingredientes',
        'tags' : '$tags',
        'autor_info' : '$autor_info'
        }}])
        recetas2 = mongo.A.aggregate([{
            '$match': {
                'autor_info.name' : {'$regex':data.get("receta")}
            }
        },
                                     {'$project':{
        'receta' : '$receta',
        'ingredientes' : '$ingredientes',
        'tags' : '$tags',
        'autor_info' : '$autor_info'
        }}])
        response2 = json_util.dumps(recetas2)
        response = json_util.dumps(recetas)
        response = json.loads(response)
        response2 = json.loads(response2)
        rsp = response2 + response
        return render_template("index.html", name = "Javi", recetas = rsp)

    else:

        recetas = mongo.A.aggregate([{'$project':{
        'receta' : '$receta',
        'ingredientes' : '$ingredientes',
        'tags' : '$tags',
        'autor_info' : '$autor_info'
        }}])
        response = json_util.dumps(recetas)
        response = json.loads(response)
        return render_template("index.html", name = "Javi", recetas = response)
    
    

@views.route("/<userid>")
def detalles(userid):
    user=userid[10:34:1]
    
    receta = mongo.A.find({'_id': ObjectId(user)})
    response=json_util.dumps(receta)
    
    response = json.loads(response)
    Aux = response[0]
    tags=""
    for  tag in Aux.get("tags"):
        if tag == Aux.get("tags")[-1]:     
            tags=tags + tag + ""
        else:
            tags=tags + tag +", "

    n_meGusta = mongo.A.aggregate([{
        '$match' : {
            '_id':ObjectId(user)
        }

    },{'$project' : {
        '_id':0,
        'likes' : {
            '$size' : '$me_gusta'
        }
    }}])

    n_meGusta = json_util.dumps(n_meGusta)
    n_meGustaDef = json.loads(n_meGusta)[0]
    return render_template("details.html", receta = response, tags = tags, mg = n_meGustaDef)


@views.route("/top_publishers")
def top():
   

    Aux = mongo.A.aggregate([{
        "$sortByCount":"$autor_info.name"},{
        "$limit" : 10
        }])

    tops = json_util.dumps(Aux)
    tops = json.loads(tops)
    print(tops)
    return render_template("top.html", top = tops)
