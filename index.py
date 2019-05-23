import os
import json
import sys
import datetime
from flask import Flask, send_from_directory, request, jsonify, make_response
from flask_pymongo import PyMongo


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))

PUBLIC_TEMPLATES = os.path.join(ROOT_PATH, 'templates')

import logger
from app import app, mongo

LOG = logger.get_root_logger(os.environ.get(
    'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))


PORT = os.environ.get('PORT')


@app.errorhandler(404)
def not_found(error):
    """ error handler """
    LOG.error(error)
    return send_from_directory(PUBLIC_TEMPLATES, "404.html")

@app.route("/")
def home():
    return send_from_directory(PUBLIC_TEMPLATES, "home.html")

@app.route("/add_node", methods = ['POST'])
def result():
	result = request.form
	node = {"mac":result["mac"], "psnt": result["psnt"]}
	x = mongo.db.nodes.insert_one(node)
	return send_from_directory(PUBLIC_TEMPLATES, "home.html")

if __name__ == "__main__":
    LOG.info('running environment: %s', os.environ.get('ENV'))
    app.config['DEBUG'] = os.environ.get('ENV') == 'development' 
    app.run(host='0.0.0.0', port=int(PORT)) 