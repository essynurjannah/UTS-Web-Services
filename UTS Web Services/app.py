#Aji Prasetyo 19090067
#Hanif Arkhan A 19090020
#Esy Nurjanah 1909009
#Naimatul Maudiah 1909008

from flask import Flask,request,jsonify
from flask_httpauth import HTTPTokenAuth
import random, os, string
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import check_password_hash
from sqlalchemy import DATETIME, TIMESTAMP

app=Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "uts_ws.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
Db = SQLAlchemy(app)

class users(Db.Model):
    username = Db.Column(Db.String(20), unique=True,nullable=False, primary_key=True)
    password = Db.Column(Db.String(20), unique=False,nullable=False, primary_key=False)
    token = Db.Column(Db.String(20), unique=False,nullable=True, primary_key=False)
    created_at = Db.Column(TIMESTAMP,default=datetime.datetime.now)
class events(Db.Model):
    event_creator = Db.Column(Db.String(20), unique=False,nullable=False, primary_key=False)
    event_name = Db.Column(Db.String(20), unique=False,nullable=False, primary_key=True)
    event_start_time = Db.Column(DATETIME, unique=False,nullable=False, primary_key=False)
    event_end_time = Db.Column(DATETIME, unique=False,nullable=False, primary_key=False)
    event_start_lat= Db.Column(Db.String(20), unique=False,nullable=False, primary_key=False)
    event_start_lng =Db.Column(Db.String(20), unique=False,nullable=False, primary_key=False)
    event_finish_lat = Db.Column(Db.String(20), unique=False,nullable=False, primary_key=False)
    event_finish_lng = Db.Column(Db.String(20), unique=False,nullable=False, primary_key=False)
    created_at = Db.Column(DATETIME,default=datetime.datetime.now)
class logs(Db.Model):
    username = Db.Column(Db.String(20), unique=True,nullable=False, primary_key=True)
    event_name = Db.Column(Db.String(20), unique=False,nullable=False, primary_key=False)
    log_lat = Db.Column(DATETIME, unique=False,nullable=False, primary_key=False)
    log_lng = Db.Column(DATETIME, unique=False,nullable=False, primary_key=False)
    created_at = Db.Column(TIMESTAMP, unique=False,nullable=False, primary_key=False)
Db.create_all()
@app.route('/api/v1/users/create/', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    user = users(username=username,password=password,token= '')
    Db.session.add(user)
    Db.session.commit()
    return jsonify({"msg" : "registrasi sukses"}), 200
@app.route('/api/v1/users/login/', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    i=15
    user= users.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
           token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = i))
           user.token= token
           Db.session.commit()
    return jsonify({"msg": "login sukses","token": token,}), 200
@app.route('/api/v1/events/create/', methods=['POST'])
def event():
    token = request.json['token']
    username=users.query.filter_by(token=token).first()
    user = str(username.username)
    event_name = request.json['event_name']
    event_start_time = request.json['event_start_time']
    event_start_time_obj = datetime.datetime.strptime(event_start_time, '%Y-%m-%d %H:%M')
    event_end_time = request.json['event_end_time']
    event_end_time_obj = datetime.datetime.strptime(event_end_time, '%Y-%m-%d %H:%M')
    event_start_lat = request.json['event_start_lat']
    event_start_lng = request.json['event_start_lng']
    event_finish_lat = request.json['event_finish_lat']
    event_finish_lng = request.json['event_finish_lng']
    eventt = events(event_creator = user,
                    event_name = event_name,
                    event_start_time = event_start_time_obj,
                    event_end_time = event_end_time_obj,
                    event_start_lat = event_start_lat,
                    event_start_lng = event_start_lng,
                    event_finish_lat = event_finish_lat,
                    event_finish_lng = event_finish_lng)
    Db.session.add(eventt)
    Db.session.commit()
    return jsonify({"msg": "membuat event sukses"}), 200
@app.route('/api/v1/events/log', methods=['POST'])
def create_logs():
    token = request.json['token']
    username=users.query.filter_by(token=token).first()
    user=str(username.username)
    print(user)
    log = logs(username = format(user), event_name = request.json['event_name'],log_lat = request.json['log_lat'], log_lng = request.json['log_lng'])
    Db.session.add(log)
    Db.session.commit()
    return jsonify({"msg": "Log berhasil dibuat"}), 200
@app.route('/api/v1/event/logs/<token>/<event_name>', methods=['GET'])
def view_logs(token,event_name):
    view= logs.query.filter_by(event_name=event_name).all()
    
    log = []

    for i in view:
        dictlogs = {}
        dictlogs.update({"username": i.username,"log_lat": i.log_lat, "log_lng": i.log_lng, "create_at": i.created_at})
        log.append(dictlogs)
    return jsonify(log), 200
if __name__ == '__main__':
  app.run(debug = True, port=5000)