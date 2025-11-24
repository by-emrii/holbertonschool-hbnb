from flask import Flask, render_template, redirect, make_response
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(
        __name__,
        template_folder="../../frontend/templates",
        static_folder="../../frontend/static"
    )

    app.config.from_object(config_class)

    CORS(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # ========================
    #   FRONT-END ROUTES
    # ========================
    
    @app.route('/')
    def index():
        return render_template('index/index.html')

    @app.route("/login")
    def login():
        return render_template("login/login.html")
    
    @app.route("/logout")
    def logout():
        resp = make_response(redirect('/'))
        resp.set_cookie('token', '', expires=0)
        return resp
    
    @app.route("/place_details")
    def place_details():
        return render_template("place_details/place_details.html")

    @app.route("/add_review")
    def add_review():
        return render_template("add_review/add_review.html")


    # ========================
    #   API ROUTES
    # ========================
    
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Import namespaces after app and db are initialized
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.admin import api as admin_ns

    # =======================
    # REGISTER NAMESPACES
    # =======================

    # Register the user namespace
    api.add_namespace(users_ns, path='/api/v1/users')

    # Register the amenity namespace
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    # Place namespace
    api.add_namespace(places_ns, path='/api/v1/places')

    # Review namespace
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    # Auth namespace
    api.add_namespace(auth_ns, path="/api/v1/auth")

    # Admin namespace
    api.add_namespace(admin_ns, path="/api/v1")

                      
    return app