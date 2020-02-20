from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import numpy as np
import os
import joblib

app = Flask(__name__)

@app.route('/predict',methods=['POST'])
def add():
    #california=float(request.form['california'])
    #florida=float(request.form['florida'])
    #newyork=float(request.form['newyork'])
    #randd=float(request.form['randd'])
    #admin=float(request.form['admin'])
    #market=float(request.form['market'])
    jsonf=request.get_json(force=True)
    california=float(jsonf.get('california'))
    florida=float(jsonf.get('florida'))
    newyork=float(jsonf.get('newyork'))
    randd=float(jsonf.get('randd'))
    admin=float(jsonf.get('admin'))
    market=float(jsonf.get('market'))
    loaded_model = joblib.load('finalized_model.sav')
    test = [florida,newyork,randd,admin,market]
    test=np.array(test)
    test=test.reshape(1,-1)
    result=loaded_model.predict(test)[0]
    return jsonify({'predict':result})


@app.route('/',methods=['GET'])
def get():
    return jsonify({'msg':'everything is good'})

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)
