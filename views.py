import json
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from pymongo import MongoClient
from bson import json_util
client = MongoClient('mongodb://localhost:27017/')
mongo = client.ProyectoCBD

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    recetas = mongo.A.find()
    response = json_util.dumps(recetas)
    response = json.loads(response)
    return render_template("index.html", name = "Javi", recetas = response)


@views.route("/tags")
def recetasXEtiquetas():
    recetas = mongo.A.aggregate([
    {"$unwind": "$tags"},
    {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
])
    response = json_util.dumps(recetas)
    response = json.loads(response)
    print(response)
    return render_template("topTags.html", name = "Javi", recetas = response)

@views.route("/sort")
def sort():
    recetas = mongo.A.aggregate([{"$sort": {"receta":1}}])
    response = json_util.dumps(recetas)
    response = json.loads(response)
    return render_template("sort.html", name = "Javi", recetas = response)

@views.route("/mostComment")
def topComment():
    recetas = mongo.A.aggregate([{
        "$match": {"post": {"$exists": True}} # solo considerar documentos que contengan el campo "post"
    },{"$project": {"_id": 1,"me_gusta": 1,"receta":1,"autor_info.name":1,"ingredientes":1,"tags":1, "num_posts": {"$size": "$post"}}},
    {"$sort": {"num_posts": -1}},
    {"$limit": 3}])
    response = json_util.dumps(recetas)
    response = json.loads(response)
    return render_template("TopComments.html", name = "Javi", recetas = response)


@views.route("/mostRated")
def topPuntuaciones():
    recetas = mongo.A.aggregate([{"$project": {"me_gusta": 1,"receta":1,"autor_info.name":1,"ingredientes":1,"tags":1,"numElements": { "$size": "$me_gusta" }}},{ "$sort": { "numElements": -1 } },{ "$limit": 3 }])
    response = json_util.dumps(recetas)
    response = json.loads(response)
    return render_template("TopPuntuaciones.html", name = "Javi", recetas = response)




@views.route("/filter/<username>")
def home2(username):
    return render_template("index.html", name = username)

@views.route("/data")
def getData():
    data = request.json
    return jsonify(data)

@views.route("/go_to_home")
def go_to_home():

    return redirect(url_for("views.home"))
