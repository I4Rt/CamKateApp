from datetime import datetime
from flask import request, json, jsonify, make_response, Response, render_template,redirect
from config import *
from model.data.CamSector import *

from model.data import *


@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def redirectMain(): 
    return redirect('/main')


@app.route('/main', methods=['get'])
@cross_origin()
def main():
    return render_template('main.html', sectors=CamSector.getAll())


@app.route('/camList', methods=['get'])
@cross_origin()
def camList():
    return render_template('cameras.html')


@app.route('/editCamera', methods=['get'])
@cross_origin()
def editCamera():
    isNew = request.args.get('new')
    if isNew:
        return render_template('camera_edit.html', cam = None)
    requestedCamId = request.args.get('id')
    camSearchResult = CamSector.getByID(requestedCamId)
    if camSearchResult:
        return render_template('camera_edit.html', cam=camSearchResult)
    return f'no camera with id {requestedCamId}'
    
@app.route('/getData', methods=['get'])
@cross_origin()
def getData():
    
    camSecs = list(map(lambda x: [x.id, x.name], CamSector.getAll())) 
    return render_template('get_csv.html', camSecs=camSecs)