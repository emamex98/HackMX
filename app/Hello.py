from flask import Flask, request, render_template, jsonify
import mysql.connector
import simplejson as json
import sys

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def hello():
    
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

    
    #result = json.dumps(resultdict)
    return jsonify(resultdict)
    #return render_template('index.html', result = result)

if __name__ == '__main__':
   app.run(debug = True)
