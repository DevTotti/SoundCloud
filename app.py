from flask import Flask
from dotenv import load_dotenv
from flask_mongoengine import MongoEngine
import os
from api.routes import api_routes
from flask_restful import Api#install
import sys


UPLOAD_FOLDER = "uploads"



load_dotenv()

default_config = {
    "MONGODB_SETTINGS": {
        'db': os.environ["APP"],
        'host': os.environ["HOST"],
        'port': 0,
    },
    "UPLOAD_FOLDER": UPLOAD_FOLDER
}



    
def initialize():
    app = Flask(__name__)
    app.config.update(default_config)
    mongo = MongoEngine(app)
    api = Api(app=app)
    api = api_routes(api=api)
    return app


    


if __name__ == '__main__':
    #to change port add port=PORT_NUMBER after debug=True
    app = initialize()
    app.run(debug=True)