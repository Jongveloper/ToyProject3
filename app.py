from flask import Flask, render_template, request, jsonify, redirect
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
            return "회원가입이 완료되었습니다!"
        return redirect(url_for('login'))

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)