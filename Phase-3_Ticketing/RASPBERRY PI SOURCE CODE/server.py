from flask import Flask, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


TEMPLATE_FOLDER_PATH = '/home/pi/Desktop/ComNet-class-project/HTMLtemplate'
STATIC_FOLDER_PATH = '/home/pi/Desktop/ComNet-class-project/static'

app = Flask(__name__, template_folder = TEMPLATE_FOLDER_PATH)
app._static_folder = STATIC_FOLDER_PATH

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pi/Desktop/ComNet-class-project/database.db'
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#declare necessary parameters
ARGO_PER_HOUR = 5000

#define table for users
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True)
    password = db.Column(db.String(30), unique = True)


#define tables in database
class log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plat = db.Column(db.String(15))
    waktu = db.Column(db.String(30))

class history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plat = db.Column(db.String(15))
    waktuMasuk = db.Column(db.String(30))
    waktuKeluar = db.Column(db.String(30))
    argo = db.Column(db.String(8))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logmein', methods = ['POST'])
def logmein():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username = username).first()
    password = User.query.filter_by(password = password).first()

    if not (user and password):
        return '<h1> wrong username/password! </h1>'

    login_user(user)

    return redirect('/mainPage')

@app.route('/')
def login():
    return render_template('loginPage.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/mainPage')

@app.route('/mainPage')
@login_required
def mainPage():
    return render_template('main.html')

#import necessary functions from utils.py
from utils import *

@app.route('/post', methods = ["POST"])
def post():
    plat = request.data
    plat = plat.decode("utf-8")
    #returns the price if detected plat in database. otherwise, write plat to database
    output = processToDatabase(plat, ARGO_PER_HOUR)

    print(output)
    
    return ''

@app.route('/purge', methods = ['GET', 'POST'])
@login_required
def purge():
    if request.method == 'POST':
        total_purged = purgeAll(history)
        return "Purged: " + str(total_purged)
    else:
        return render_template('purge.html')

@app.route('/viewLog')
@login_required
def viewLog():
    from server import db, log

    all_query = db.session.query(log).all()
    data_count = len(all_query)

    
    return render_template('viewLog.html', data = all_query, data_count = data_count)

@app.route('/viewHistory')
@login_required
def viewHistory():
    from server import db, history

    all_query = db.session.query(history).all()
    data_count = len(all_query)

    
    return render_template('viewHistory.html', data = all_query, data_count = data_count)

@app.route('/aboutUs')
@login_required
def aboutUs():
    return render_template('aboutUs.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 8090)
