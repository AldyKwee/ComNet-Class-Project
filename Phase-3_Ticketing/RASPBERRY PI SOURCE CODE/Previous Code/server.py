from flask import Flask, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy

TEMPLATE_FOLDER_PATH = '/home/pi/Desktop/ComNet-class-project/HTMLtemplate'
STATIC_FOLDER_PATH = '/home/pi/Desktop/ComNet-class-project/static'

app = Flask(__name__, template_folder = TEMPLATE_FOLDER_PATH)
app._static_folder = STATIC_FOLDER_PATH

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pi/Desktop/ComNet-class-project/database.db'
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

#declare necessary parameters
ARGO_PER_HOUR = 5000

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

@app.route('/')
def main():
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
def purge():
    if request.method == 'POST':
        total_purged = purgeAll(history)
        return "Purged: " + str(total_purged)
    else:
        return render_template('purge.html')

@app.route('/viewLog')
def viewLog():
    from mq_new import db, log

    all_query = db.session.query(log).all()
    data_count = len(all_query)

    
    return render_template('viewLog.html', data = all_query, data_count = data_count)

@app.route('/viewHistory')
def viewHistory():
    from mq_new import db, history

    all_query = db.session.query(history).all()
    data_count = len(all_query)

    
    return render_template('viewHistory.html', data = all_query, data_count = data_count)

@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 8090)
