from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
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

url = ''
user_tid = ''

@app.route('/sign-up', methods=['POST'])
def register():
    global url
    global user_tid
    data = request.get_json(force=True)
    new_user = User(data)
    try:
        db.session.add(new_user)
        db.session.commit()
        user_tid = new_user.typing_id
        return {
            'status': 'success',
            'msg': 'user created successfully',
            'url':  url+'/2fa'
        }, 201
    except IntegrityError:
        return {
            'status': 'error',
            'msg': 'User with email {} already exists'.format(data['email'])
        }, 400

@app.route('/sendtypingdata', methods=['POST'])
def sendtypingdata():
    data = request.get_json(force=True)
    print(data)
    res = send_typing_data(data['user_tid'], data['pattern'])
    return res


@app.route('/2fa')
def twofa():
    print(user_tid)
    return render_template('index.html', user_tid=user_tid)


if __name__ == '__main__':
    app.run()
