from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("reviews", description="Review operations")

# Model for creating a review
review_create_model = api.model('ReviewCreate', {
    "user_id": fields.String(required=True, description="User ID of the reviewer"),
    "place_id": fields.String(required=True, description="Place ID being reviewed"),
    "rating": fields.Float(required=True, description="Rating (1-5)", min=1, max=5),
    "comment": fields.String(required=True, description="Review comment"),
    "upload_image": fields.List(fields.String, required=False, description="Optional image URLs")
})

# Model for updating a review
review_update_model = api.model('ReviewUpdate', {
    "rating": fields.Float(required=False, description="Rating (1-5)", min=1, max=5),
    "comment": fields.String(required=False, description="Review comment"),
    "upload_image": fields.List(fields.String, required=False, description="Optional image URLs"),
    "current_user_id": fields.String(required=False, description="ID of the user performing update")
})

# Model for response
review_response_model = api.model('Review', {
    "id": fields.String,
    "user_id": fields.String,
    "place_id": fields.String,
    "rating": fields.Float,
    "comment": fields.String,
    "upload_image": fields.List(fields.String)
})


"""Create a review for a place"""
@api.route('/')
class ReviewList(Resource):
    @api.expect(review_create_model, validate=True)
    @api.marshal_with(review_response_model, code=201)
    def post(self):
        """Creating a review"""
        try:
            review_data = api.payload
            review = facade.create_review(review_data)
            return review.save(), 201
        except ValueError as e:
            return {"error": str(e)}, 400
        
    @api.marshal_list_with(review_response_model, code=200)
    def get(self):
        """List all reviews for a specific place"""
        place_id = request.args.get("place_id")
        reviews = (
            facade.get_reviews_for_place(place_id)
            if place_id else
            facade.review_service.review_repo.get_all()
        )
        if not reviews:
            return {"message": "No reviews found"}, 404
        return [r.save() for r in reviews], 200

"""Get, update, deleted review by id"""
@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.marshal_with(review_response_model, code=200)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review by id"""
        try:
            review = facade.get_review(review_id)
            return review, 200
        except ValueError as e:
            return {"error": str(e)}, 404

    @api.expect(review_update_model, validate=True)
    @api.marshal_with(review_response_model, code=200)
    @api.response(403, 'Forbidden')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review"""
        try:
            data = api.payload or {}
            current_user_id = data.get("current_user_id")
            review = facade.update_review(review_id, data, current_user_id)
            return review, 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except PermissionError as e:
            return {"error": str(e)}, 403

    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete review"""
        result = facade.delete_review(review_id)
        if isinstance(result, dict) and "error" in result:
            return result, 404
        return {"message": "Review deleted successfully"}, 200
    
"""List all reviews of place"""
@api.route('/place/<string:place_id>')
class ReviewsByPlace(Resource):
    @api.marshal_list_with(review_response_model, code=200)
    @api.response(404, 'No reviews found for this place')
    def get(self, place_id):
        """List all reviews for a specific place."""
        reviews = facade.get_reviews_for_place(place_id)
        if not reviews:
            return {"message": f"No reviews found for place_id '{place_id}'"}, 404
        return [r.save() for r in reviews], 200

"""List review of user"""
@api.route('/user/<string:user_id>')
class ReviewsByUser(Resource):
    @api.marshal_list_with(review_response_model, code=200)
    @api.response(404, 'No reviews found for user')
    def get(self, user_id):
        """List all reviews made by a specific user"""
        reviews = facade.get_reviews_by_user(user_id)
        if not reviews:
            return {"message": f"No reviews found for user_id '{user_id}'"}, 404
        return [r.save() for r in reviews], 200