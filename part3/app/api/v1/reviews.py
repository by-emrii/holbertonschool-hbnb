from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace("reviews", description="Review operations")

# Model for creating a review
review_create_model = api.model('ReviewCreate', {
    "place_id": fields.String(required=True),
    "rating": fields.Integer(required=True, min=1, max=5),
    "text": fields.String(required=True),
    "upload_image": fields.List(fields.String, required=False)
})

# Model for updating a review
review_update_model = api.model('ReviewUpdate', {
    "rating": fields.Integer(required=True, min=1, max=5),
    "text": fields.String(required=True, max_length=300),
    "upload_image": fields.List(fields.String, required=False),
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
    @jwt_required() 
    @api.expect(review_create_model, validate=True) 
    #@api.marshal_with(review_response_model, code=201) 
    def post(self): 
        """Create a review""" 
        data = api.payload 
        current_user = get_jwt_identity() 

        try:
            # Get place first
            place = facade.get_place(data["place_id"])
            if not place:
                return {'error': 'Place not found'}, 404

            # Owners cannot review their own place (optional)
            if place.owner_id == current_user:
                return {'error': "You cannot review your own place."}, 400
            
            # User can only review a place once
            if facade.user_already_reviewed(place.id, current_user):
                return {'error': "You have already reviewed this place."}, 400

            # Fetch user object (depends on how your facade works)
            user = facade.get_user(current_user)
            if not user:
                return {'error': 'User not found'}, 404

            # Now create the review, passing real objects if your facade requires them
            review = facade.create_review({
                "user": user,
                "place": place,
                "rating": data["rating"],
                "text": data["text"],
                "upload_image": data.get("upload_image", []),
            })

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

    @jwt_required()
    @api.expect(review_update_model, validate=True)
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorised action')
    def put(self, review_id):
        """Update a review (owner only)"""
        data = api.payload or {}
        current_user = get_jwt_identity()
        
        try:
            review = facade.get_review_by_id(review_id)
            if review.user.id != current_user:
                return {"error": 'Unauthorised action'}, 403
            
            #update the review
            update = facade.update_review(review_id, data, current_user)
            return update.to_dict(), 200
        
        except PermissionError as e:
            return {"error": str(e)}, 403
        except ValueError as e:
            return {"error": str(e)}, 404

    @jwt_required()     
    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review (owner only)"""
        current_user = get_jwt_identity()

        try:
            # check there a review 
            review = facade.get_review_by_id(review_id)
            if review is None:
                return {"error": "Review not found"}, 404
            # Ownership check
            user_id = getattr(review.user, "id", review.user)
            if str(user_id) != str(current_user):
                return {"error": "Unauthorized action."}, 403
            
            # Delete the review
            facade.delete_review(review_id, current_user)
            return {"message": "Review deleted successfully"}, 200

        except Exception as e:
            return {"error": str(e)}, 500
    
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