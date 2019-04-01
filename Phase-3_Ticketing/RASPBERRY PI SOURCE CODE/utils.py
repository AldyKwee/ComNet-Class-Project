from datetime import datetime
import numpy as np
from mq_new import db, log, purge

def getDateTime():
    return datetime.now()

def checkDatabase(platNomor):
    allQuery = log.query.all()

    for i in range(0, len(allQuery)):
        if str(platNomor) == str(allQuery[i].plat):
            return "exist"
    return "not exist"

def calculateParkingPrice(waktuMasuk, waktuKeluar, ARGO_PER_HOUR):
    difference = waktuKeluar - waktuMasuk
    differenceInSecond = difference.total_seconds()
    hoursParked = np.ceil(differenceInSecond / 3600)
    price = hoursParked * ARGO_PER_HOUR
    return price


def processToDatabase(data, ARGO_PER_HOUR):
    '''data = plat mobil
    argo per hour = bisa di tentukan di main code'''
    #preparing the data
    waktu = getDateTime()
    platNomor = str(data)


    #writing to database

    #checking if the car already inside
    databaseChecker = checkDatabase(platNomor)

    #if not exist in database, then the car is going in
    if not platNomor == "":
        if databaseChecker == "not exist": 
            db.session.add(log(plat = str(platNomor), waktu = waktu))
            db.session.commit()
            return "Welcome " + str(platNomor) + ". Successfully write to database"
        else:
        #if exist in database, then the car is going out
            tempIndex = log.query.filter_by(plat = platNomor).first()
            waktuMasuk = datetime.strptime(tempIndex.waktu, '%Y-%m-%d %H:%M:%S.%f')
            waktuKeluar = waktu
            log.query.filter_by(plat = str(platNomor)).delete()
            db.session.add(purge(plat = str(platNomor), waktuMasuk = waktuMasuk, waktuKeluar = waktu))
            db.session.commit()
            return calculateParkingPrice(waktuMasuk, waktuKeluar, ARGO_PER_HOUR)
 
def purgeAll(purge):
    try:
        num_rows_deleted = db.session.query(purge).delete()
        db.session.commit()
        return num_rows_deleted
    except:
        db.session.rollback()

