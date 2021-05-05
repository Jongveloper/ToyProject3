from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from flask_jwt_extended import *
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# JWT 매니저 활성화

app.config['JWT_COOKIE_SECURE'] = False #https를 통해서만 쿠키가 갈 수 있는지 프로덕션에선 True
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/' # access 쿠키를 보관할 url
app.config['JWT_REFRESH_COOKIE_PATH'] = '/' # refresh 쿠키를 보관할 url
app.config['JWT_COOKIE_CSRF_PROTECT'] = True

# 몽고 db
client = MongoClient('localhost', 27017)
db = client.dbname

@app.route('/')
def home():
    return render_template('login.html')
@app.route('/main')
def main():
    return render_template('main.html')

#회원가입
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("sign_up.html")
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        userid = request.form.get('userid')
        password = request.form.get('password')
        re_password = request.form.get('re_password')

        doc = {'user_id': userid, 'user_name': username, 'user_pw': password, 'user_mail': email}

        if not (userid and username and password and re_password and email):
            return "모두 입력해주세요!"
        elif password != re_password:
            return "비밀번호가 일치하지 않습니다."
        else:
            db.users.insert_one(doc)
            return redirect(url_for('login'))   
# 로그인
app.secret_key = 'dkdkdkdk2'

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        userid = request.form['userid']
        password = request.form['password']

        members = db.users.find_one({'user_id': userid, 'user_pw': password})

        if members is None:
            return '아이디 비밀번호를 확인해주세요'
        else:
            session['user'] = userid
            return render_template('main.html')

@app.route('/reservation')
def reservation():
    return render_template('reservation.html')

#예약하기 (POST) API
@app.route('/user', methods=['POST'])
def save_people():
    name_receive = request.form['name_give']
    day_receive = request.form['day_give']
    phone_receive = request.form['phone_give']

    doc = {
        'name': name_receive,
        'day': day_receive,
        'phone': phone_receive
    }
    db.people.insert_one(doc)

    return jsonify({'msg': '예약이 완료되었습니다!'})

#예약 목록 보기 (GET) API
@app.route('/user', methods=['GET'])
def view_people():
    rese = list(db.people.find({}, {'_id': False}))
    return jsonify({'user': rese})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)