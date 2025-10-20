from flask import request, send_file
from flask_restx import Namespace, Resource, fields
from app.services import HBnBFacade

api = Namespace("reviews", description="Review operations")
facade = HBnBFacade()

# Review input/output model
review_model = api.model('Review', {
    "user_id": fields.String(required=True, description="ID of the user"),
    "place_id": fields.String(required=True, description="ID of the place"),
    "rating": fields.Float(required=True, description="Rating (1-5)", min=1, max=5),
    "comment": fields.String(required=True, description="Review comment"),
    "upload_image": fields.List(fields.String, required=False, description="Optional image URLs")
})

"""Create and list all reviews"""
@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Creating a review"""
        review_data = request.get_json()
        result = facade.create_review(review_data)
        if isinstance(result, dict) and "error" in result:
            return result, 400
        return result.save(), 201

    @api.response(200, 'Success')
    def get(self):
        """lists all reviews"""
        reviews = facade.get_all_reviews()
        return [review.save() for review in reviews], 200

"""Retrieve, update, deleted review by user id"""
@api.route('/<string:review_id>')
class ReviewDetail(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review by review id"""
        review = facade.get_review_by_id(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.save(), 200

    @api.expect(review_model)
    @api.response(200, 'Review successfully updated')
    @api.response(403, 'Not allowed')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review"""
        review_data = request.get_json() or {}
        current_user_id = review_data.get("current_user_id")
        try:
            updated_review = facade.update_review({
                "review_id": review_id,
                "review_data": review_data,
                "current_user_id": current_user_id
            })
            return updated_review.save(), 200
        except (ValueError, PermissionError) as error:
            return {"error": str(error)}, 403

    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete review"""
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted"}, 200
        except ValueError as error:
            return {"error": str(error)}, 404
        
"""List reviews by place id"""
@api.route('/place/<string:place_id>')
class ReviewByPlace(Resource):
    @api.response(200, 'Success')
    def get(self, place_id):
        """List all reviews of a place"""
        reviews = facade.get_reviews_for_place(place_id)
        if not reviews:
            return {"message": f"No reviews found for place_id '{place_id}'"}, 404
        return [r.save() for r in reviews], 200

"""List review of user"""
@api.route('/user/<string:user_id>')
class ReviewByUser(Resource):
    @api.response(200, 'Success')
    def get(self, user_id):
        """List all reviews made by a specific user"""
        reviews = facade.get_reviews_by_user(user_id)
        if not reviews:
            return {"message": f"No reviews found for user_id '{user_id}'"}, 404
        return [r.save() for r in reviews], 200
