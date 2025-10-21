from flask import request, send_file
from flask_restx import Namespace, Resource, fields
from app.services import HBnBFacade

api = Namespace("reviews", description="Review operations")
facade = HBnBFacade()

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
    "upload_image": fields.List(fields.String, required=False, description="Optional image URLs")
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
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Creating a review"""
        review_data = request.get_json() or {}
        try:
            review = facade.create_review(review_data)
        except ValueError as ve:
            return {"error": str(ve)}, 400
        return review.save(), 201
    
    @api.response(200, 'Success')
    def get(self):
        """List all reviews for a specific place"""
        place_id = request.args.get("place_id")
        if place_id:
            reviews = facade.get_reviews_for_place(place_id)
        else:
            reviews = facade.review_service.review_repo.get_all()

        if not reviews:
            return {"message": "No reviews found"}, 404
        return [r.save() for r in reviews], 200

"""Get, update, deleted review by id"""
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

    @api.expect(review_update_model)
    @api.response(200, 'Review successfully updated')
    @api.response(403, 'Not allowed')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review"""
        review_data = request.get_json() or {}
        current_user_id = review_data.get("current_user_id")

        updated_review = facade.update_review({
                "review_id": review_id,
                "review_data": review_data,
                "current_user_id": current_user_id
        })
        if isinstance(updated_review, dict) and "error" in updated_review:
            return updated_review, 403
        return updated_review.save(), 200

    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete review"""
        result = facade.delete_review(review_id)
        if isinstance(result, dict) and "error" in result:
            return result, 404
        return {"message": "Review deleted"}, 200

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
