from flask_restx import Namespace, Resource, fields
from app.services import facade

api = namespace("reviews", description="Review operations")

reviews = [
  {"userId": fields.String(required=True)}, 
  {"placeId": fields.String(required=True)},
  {"rating": fields.Float(required=True, min=1, max=5)},
  {"comment": fields.String(required=True)},
  {"upload_image": fields.List(fields.String, required=False)},
]

"""Review list"""
@api.get("/reviews")
def get_review():
    return reviews

@api.post("/reviews")
def post_review(reviews):
    reviews = request.get_json()
    reviews.append(reviews)
    return reviews, 200

"""Review specific list"""
@api.get("/reviews")
def get_review():
    return reviews

@api.post("/reviews")
def post_review(reviews):
    reviews = request.get_json()
    reviews.append(reviews)
    return reviews, 200


"""Delete list"""



put
delete



