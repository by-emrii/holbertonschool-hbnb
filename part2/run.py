from app import create_app
from flask import Flask
from flask_restx import Api
from app.api.v1.reviews import api as reviews_api

#app = create_app()

#if __name__ == '__main__':
 #   app.run(debug=True)

def create_app():
  app = Flask(__name__)
  api = Api(app, version="1.0", title="HBNH API", description="API for HBNB")
  api.add_namespace(reviews_api, path="/api/v1/reviews")

  return app