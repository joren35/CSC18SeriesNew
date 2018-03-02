#!flask/bin/python
from flask import Flask, jsonify,request
from model import DBconn
import flask
import sys,os

app = Flask(__name__)

def spcall(qry, param, commit=False):
    try:
        dbo = DBconn()
        cursor = dbo.getcursor()
        cursor.callproc(qry, param)
        res = cursor.fetchall()
        if commit:
            dbo.dbcommit()
        return res
    except:
        res = [("Error: " + str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]),)]
    return res


@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'working'})

@app.route('/user', methods=['GET'])
def getAllUserID():

    res = spcall('getAllUserID', ())

    recs = []

    for r in res:
        recs.append({"ID": r[0], "Username": r[1], "Name": r[2]})

    return jsonify({'status': 'ok', 'entries': recs, 'count': len(recs)})

@app.route('/user/<string:number>', methods=['GET'])
def getOneUserID(number):

    res = spcall('getOneUserID', (number))

    recs = []

    for r in res:
        recs.append({"ID": r[0], "Username": r[1], "Name": r[2]})

    return jsonify({'status': 'ok', 'entries': recs, 'count': len(recs)})


@app.route('/registration', methods=['POST'])
def addUser():

    params = request.get_json()
    username = params["username"]
    name = params["name"]

    res = spcall('addUser',(username,name), True)

    if 'ok' in res[0][0]:
        return jsonify({'status': 'Added'})

@app.route('/delete/<string:userID>', methods=['DELETE'])
def deleteUser(userID):

    res = spcall('deleteUser', (userID), True)
    if 'ok' in res[0][0]:
        return jsonify({'status': 'Deleted'})
    else:
        return jsonify({'status:' 'Error'})



@app.route('/update/<string:idNumber>', methods=['PUT'])
def updateUser(idNumber):

    params = request.get_json()
    newUsername = params["newUsername"]

    res = spcall('updateUser', (idNumber,newUsername), True)

    if 'ok' in res[0][0]:
        return jsonify({'status': 'Updated'})
    else:
        return jsonify({'status:' 'Error'})


if __name__ == '__main__':
    app.run(threaded=True,debug=True)