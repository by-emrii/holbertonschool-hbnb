from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("reviews", description="Review operations")

# Model for creating a review
review_create_model = api.model('ReviewCreate', {
    "user_id": fields.String(required=True),
    "place_id": fields.String(required=True),
    "rating": fields.Integer(required=True, min=1, max=5),
    "text": fields.String(required=True),
    "upload_image": fields.List(fields.String, required=False)
})

# Model for updating a review
review_update_model = api.model('ReviewUpdate', {
    "rating": fields.Integer(required=False, min=1, max=5),
    "text": fields.String(required=False, max_length=300),
    "upload_image": fields.List(fields.String, required=False),
    "current_user_id": fields.String(required=True)  # ownership check
})

# Model for response
review_response_model = api.model('Review', {
    "id": fields.String,
    "user_id": fields.String,
    "place_id": fields.String,
    "rating": fields.Integer,
    "text": fields.String,
    "upload_image": fields.List(fields.String),
    "created_at": fields.String,
    "updated_at": fields.String,
})

"""Create a review for a place"""
@api.route('/')
class ReviewList(Resource):
    @api.expect(review_create_model, validate=True)
    @api.marshal_with(review_response_model, code=201)
    def post(self):
        """Create a review"""
        data = api.payload
        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

"""Get, update, deleted review by id"""
@api.route('/<string:review_id>')
class ReviewResource(Resource):

    @api.marshal_with(review_response_model, code=200)
    def get(self, review_id):
        """Get a single review by ID"""
        try:
            review = facade.get_review_by_id(review_id)
            return review.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 404

    @api.expect(review_update_model, validate=True)
    @api.marshal_with(review_response_model, code=200)
    def put(self, review_id):
        """Update a review (owner only)"""
        data = api.payload or {}
        current_user_id = data.pop("current_user_id", None)
        try:
            review = facade.update_review(review_id, data, current_user_id)
            return review.to_dict(), 200
        except PermissionError as e:
            return {"error": str(e)}, 403
        except ValueError as e:
            return {"error": str(e)}, 404
        
    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review (owner only)"""
        current_user_id = request.args.get("current_user_id")
        try:
            result = facade.delete_review(review_id, current_user_id)
            return result, 200
        except PermissionError as e:
            return {"error": str(e)}, 403
        except ValueError as e:
            return {"error": str(e)}, 404
    
"""List all reviews of place"""
@api.route('/place/<string:place_id>')
class ReviewsByPlace(Resource):
    @api.marshal_list_with(review_response_model, code=200)
    def get(self, place_id):
        """List all reviews for a specific place"""
        reviews = facade.get_reviews_for_place(place_id)
        # Return empty list if none
        return [r.to_dict() for r in reviews], 200

"""List review of user"""
@api.route('/user/<string:user_id>')
class ReviewsByUser(Resource):
    @api.marshal_list_with(review_response_model, code=200)
    def get(self, user_id):
        """List all reviews made by a specific user"""
        reviews = facade.get_reviews_by_user(user_id)
        # Return empty list if none
        return [r.to_dict() for r in reviews], 200