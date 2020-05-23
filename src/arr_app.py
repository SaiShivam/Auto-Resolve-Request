"""
    Importing the Module
"""
import json
import os
import sys
sys.path.append(os.getcwd())
import time
import data_preprocessing
import location
import pickle
import warnings
import numpy as np
from flask import Flask, request, jsonify
import pandas as pd
import data_extraction
warnings.filterwarnings("ignore")
from flask_cors import CORS
from applogger import logger_setup


LOGGER = logger_setup('Autoresolve')
app = Flask(__name__)
CORS(app)

DATAPROCESS = data_preprocessing.DataWrangling()
LOC = location.DataLocations()
PATH = LOC.model_location()
EXTRACT = data_extraction.InternalSitesGetModifyAccess()
MODEL = pickle.load(open(str(PATH) + '/DT_model.pkl', 'rb'))



@app.route('/arr/api/v1.0/inputdata',methods=['POST'])
def post_data():
    """
        This function accepts  the new data and return the Recommendation.
    """
    start_time1 = int(round(time.time()))
    LOGGER.info("'*******************************prediction  started********************************'")
    try:
        data = request.get_json(force=True)
        data = pd.DataFrame([data], columns=data.keys())
        data = DATAPROCESS.preprocessing(data)
    except Exception as err:
        LOGGER.error(err, exc_info=True)
    data = DATAPROCESS.tokenizeandcleanData(data)
    X = DATAPROCESS.tfidf_transform(data['tokens_withoutstop'])
    data['Recommendation'] = MODEL.predict(X)
    with open(os.getcwd()+'/src/Rmap.json') as json_file:
        rmap = json.load(json_file)
    bool_intent = data['Recommendation'][0] in rmap
    data['IsSupported'] = data['Recommendation'][0] in rmap
    data['Confidence'] = np.amax(MODEL.predict_proba(X) * 100)
    extraction = EXTRACT.data_extraction(data)
    extraction = extraction.to_dict(orient='records')
    extraction = extraction[0]
    site_name = len(extraction['SiteName']) != 0
    email_id = len(extraction['UserEnterpriseId']) != 0
    extraction['IsSupported'] = bool_intent and site_name and email_id
    LOGGER.info(extraction)
    LOGGER.info("'*******************************prediction  completed********************************'")
    time_diff1 = int(round(time.time())) - start_time1
    LOGGER.info('Prediction - ELAPSED_TIME - ' + str(time_diff1))
    return jsonify(extraction)





