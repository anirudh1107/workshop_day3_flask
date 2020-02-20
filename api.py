from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

ma=Marshmallow(app)

class Profile(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    roll=db.Column(db.String(200),nullable=False)
    branch=db.Column(db.String(200),nullable=False)

    def __init__(self,name,roll,branch):
        self.name=name
        self.roll=roll
        self.branch=branch

class ProfileSchema(ma.Schema):
    class Meta:
        fields=('id','name','roll','branch')

profile_schema=ProfileSchema()
profiles_schema=ProfileSchema(many=True)

@app.route('/profile',methods=['POST','PUT'])
def add():
    name=request.form['name']
    roll=request.form['roll']
    branch=request.form['branch']
    new_profile=Profile(name,roll,branch)
    db.session.add(new_profile)
    db.session.commit()
    return profile_schema.jsonify(new_profile)

@app.route('/change',methods=['PUT'])
def change():
    id=request.form['id']
    name=request.form['name']
    roll=request.form['roll']
    branch=request.form['branch']
    profile=Profile.query.get(id)
    profile.name=name
    profile.roll=roll
    profile.branch=branch
    db.session.commit()
    return profile_schema.jsonify(profile)

@app.route('/profile/<id>',methods=['GET'])
def get_all(id):
    profile=Profile.query.get(id)
    return profile_schema.jsonify(profile)

@app.route('/userprofile',methods=['GET'])
def get_single():
    all_profiles=Profile.query.all()
    result=profiles_schema.dump(all_profiles)
    return jsonify(result)

@app.route('/',methods=['GET'])
def get():
    return jsonify({'msg':'everything is good'})

if __name__ == "__main__":
    app.run(debug=True)
