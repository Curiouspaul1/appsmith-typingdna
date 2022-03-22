from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
from flask_cors import CORS
from sendtp import send_typing_data
import os

load_dotenv()

base_dir = os.path.abspath(os.getcwd())

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{base_dir}/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('secret')
CORS(app)

db = SQLAlchemy(app)
from models import *
db.create_all()

# url = ''
# user_tid = ''

@app.route('/sign-up', methods=['POST'])
def register():
    global url
    global user_tid
    data = request.get_json(force=True)
    new_user = User(data)
    try:
        db.session.add(new_user)
        db.session.commit()
        resp =  {
            'status': 'success',
            'msg': 'user created successfully'
        }, 201
    except IntegrityError:
        resp = {
            'status': 'error',
            'msg': 'User with email {} already exists'.format(data['email'])
        }, 400
    return resp

@app.route('/sign-in', methods=['POST'])
def login():
    global user_tid
    data = request.get_json(force=True)
    # find user
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return {
            'status': 'error',
            'msg': f"No user with email {data['email']}"
        }, 400
    if not check_password_hash(user.password, data['password']):
        return {
            'status': 'error',
            'msg': f"Password incorrect"
        }, 401
    return {
        'status': 'success',
        'msg': 'Logged in successful'
    }, 200

@app.route('/sendtypingdata', methods=['POST'])
def sendtypingdata():
    data = request.get_json(force=True)
    print(data)
    print(os.getenv('tpkey'))
    res = send_typing_data(data['user_tid'], data['pattern'])
    return res


@app.route('/2fa/<email>')
def twofa(email):
    # find user with email
    user = User.query.filter_by(email=email).first()
    if user:
        return render_template('index.html', user_tid=user.typing_id)
    else:
        return render_template('404.html', email=email)
    
if __name__ == '__main__':
    app.run()
