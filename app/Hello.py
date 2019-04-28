from flask import Flask, request, render_template, jsonify, Response
import mysql.connector
import simplejson as json
import sys
import pymongo
import flask_csv
import tablib
import os

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
#app.add_url_rule('/', 'sat', hello)

@app.route('/api/sat/fisica/')
def satFisica():
    
    mydb = mysql.connector.connect(
        host="104.248.69.124",
        user="api",
        passwd="2NF7b46nWecLekQe",
        database="sat-db"
    )
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM `TRIBUTARIOS_FISICOS` WHERE rfc = '" + request.args['rfc'] + "'")
    myresult = mycursor.fetchall()

    
    resultdict = {'rfc':myresult[0][0], 
                  'nombre':myresult[0][1], 
                  'apellido_paterno':myresult[0][2], 
                  'apellido_materno':myresult[0][3],
                  'fecha_nacimiento':myresult[0][4].strftime('%Y-%m-%d'),
                  'ingresos_mensuales':myresult[0][5],
                  'score_sat':myresult[0][6]
                 } 

    return jsonify(resultdict)

@app.route('/api/sat/moral/')
def satMoral():
    
    mydb = mysql.connector.connect(
        host="104.248.69.124",
        user="api",
        passwd="2NF7b46nWecLekQe",
        database="sat-db"
    )
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM `TRIBUTARIOS_MORALES` WHERE rfc = '" + request.args['rfc'] + "'")
    myresult = mycursor.fetchall()
    
    resultdict = {'rfc':myresult[0][0], 
                  'nombre':myresult[0][1],
                  'fecha_constitucion':myresult[0][2].strftime('%Y-%m-%d'),
                  'ingresos_mensuales':myresult[0][3],
                  'score_sat':myresult[0][4]
                 } 

    return jsonify(resultdict)

@app.route('/api/buro/fisica/')
def bcFisica():
    
    mydb = mysql.connector.connect(
        host="104.248.69.124",
        user="api",
        passwd="2NF7b46nWecLekQe",
        database="bc-db"
    )
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM `CREDITICIOS_FISICOS` WHERE rfc = '" + request.args['rfc'] + "'")
    myresult = mycursor.fetchall()

    
    resultdict = {'rfc':myresult[0][0], 
                  'nombre':myresult[0][1], 
                  'apellido_paterno':myresult[0][2], 
                  'apellido_materno':myresult[0][3],
                  'fecha_nacimiento':myresult[0][4].strftime('%Y-%m-%d'),
                  'ingresos_mensuales':myresult[0][5],
                  'score_bc':myresult[0][6]
                 } 

    return jsonify(resultdict)

@app.route('/api/buro/moral/')
def bcMoral():
    
    mydb = mysql.connector.connect(
        host="104.248.69.124",
        user="api",
        passwd="2NF7b46nWecLekQe",
        database="bc-db"
    )
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM `CREDITICIOS_MORALES` WHERE rfc = '" + request.args['rfc'] + "'")
    myresult = mycursor.fetchall()
    
    resultdict = {'rfc':myresult[0][0], 
                  'nombre':myresult[0][1],
                  'fecha_constitucion':myresult[0][2].strftime('%Y-%m-%d'),
                  'ingresos_mensuales':myresult[0][3],
                  'score_bc':myresult[0][4]
                 } 

    return jsonify(resultdict)

@app.route('/api/banco/fisica/')
def bancoFisica():
    
    myclient = pymongo.MongoClient("mongodb://104.248.69.124/")

    dblist = myclient.list_database_names()
    if "BANCO" in dblist:
        mydb = myclient["BANCO"] 
  
    collist = mydb.list_collection_names()
    if "CLIENTES" in collist:
        mycol = mydb["CLIENTES"]
    
    curp = request.args['curp']
    result = mycol.find_one({'curp':curp},{'_id':0})
    return jsonify(result)

@app.route('/api/banco/all/')
def bancoAll():
    
    myclient = pymongo.MongoClient("mongodb://104.248.69.124/")

    dblist = myclient.list_database_names()
    if "BANCO" in dblist:
        mydb = myclient["BANCO"] 
  
    collist = mydb.list_collection_names()
    if "CLIENTES" in collist:
        mycol = mydb["CLIENTES"]
    
    #df =  mycol.find({},{'_id':0})
    #df =  list(df)
    #flask_csv.send_csv(df, "clientes-total.csv", ['curp', 'nombre', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'edad', 'sexo', 'nivel_trabajo', 'casa', 'ahorros', 'cheques', 'credito_cantidad', 'credito_duracion', 'credito_proposito', 'riego'])
    
    strCSV = ""
    with open('clientes-total.csv') as f:
        strCSV += f.read() + '\n'
    return strCSV
    

if __name__ == '__main__':
   app.run(debug = True)
