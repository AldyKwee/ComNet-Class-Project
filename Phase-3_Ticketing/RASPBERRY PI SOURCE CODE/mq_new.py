from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder = '/home/pi/Desktop/ComNet-class-project/HTMLtemplate')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pi/Desktop/ComNet-class-project/database.db'
app.config['SECRET_KEY'] = 'thisissecret'

db = SQLAlchemy(app)

#declare necessary parameters
ARGO_PER_HOUR = 5000

#define tables in database
class log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plat = db.Column(db.String(10))
    waktu = db.Column(db.String(30))

class purge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plat = db.Column(db.String(10))
    waktuMasuk = db.Column(db.String(30))
    waktuKeluar = db.Column(db.String(30))

from utils import *

@app.route('/post', methods = ["POST"])
def post():
    plat = request.data   
    plat = plat.decode("utf-8")

    #returns the price if detected plat in database. otherwise, write plat to database
    output = processToDatabase(plat, ARGO_PER_HOUR)

    print(output)
    
    return ''

@app.route('/homepurge', methods = ['GET', 'POST'])
def purge():
    if request.method == 'POST':
        total_purged = purgeAll(purge)
        return "Purged: " + str(total_purged)
    else:
        return render_template('homepurge.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 8090)
