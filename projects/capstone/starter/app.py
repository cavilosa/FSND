import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  @app.route("/")
  def get_greeting():
      excited = "Maryna"
      test = os.environ["SECRET"]
      greeting = f"Hello, {test}" 
     
      if excited == 'true': greeting = greeting + "!!!!!"
      return greeting

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)