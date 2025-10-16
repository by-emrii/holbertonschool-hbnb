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

"""Create a Review"""
@api.route('/')
class ReviewList(Resource):
    @api.expect(review)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Creating a review"""
        review_data = request.get_json()
        result = facade.create_review(review_data)
        if isinstance(result, dict) and "error" in result:
            return result, 400
        return result, 201

    @api.response(200, 'Success')
    def get(self):
        """lists all reviews"""
        return facade.review_service.review_repo.get_all()

"""Retrieve, update, deleted review by user id"""
@api.route('/<string:review_id>')
class ReviewDetail(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'Review not found')
    def get(self, user_id):
        """Get review by user id"""
        review = facade.get_review_by_id(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.save(), 200

    @api.expect(review_model)
    @api.response(200, 'Review successfully updated')
    @api.response(403, 'Not allowed')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """update a review"""
        review_data = request.get_json()
        current_user_id = review_data.get("current_user_id")
        try:
            return facade.update_review({
                "review_id": review_id,
                "review_data": review_data,
                "current_user_id": current_user_id
            })
        except (ValueError, PermissionError) as error:
            return {"error": str(error)}, 403
    
    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    def get_user_review():
        """Delete review"""
        try:
            return facade.delete_review(review_id)
        except ValueError as error:
            return {"error": str(error)}, 404

"""List reviews by place id"""
@api.route('/place/<string:place_id>')
class ReviewByPlace(Resource):
    @api.response(200, 'Success')
    def get(self, place_id):
        """List all reviews of a place"""
        return facade.get_review_for_place(place_id)

"""List review of user"""
@api.route('/user/<string:user_id>')
class ReviewByUser(Resource):
    @api.response(200, 'Success')
    def get(self, user_id):
        """get all of users reviews"""
        return facade.get_reviews_by_user(user_id)




