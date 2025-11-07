from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace("reviews", description="Review operations")

# Model for creating a review
review_create_model = api.model('ReviewCreate', {
    "place_id": fields.String(required=True, description="ID of the place being reviewed"),
    "rating": fields.Integer(required=True, min=1, max=5, description="Rating between 1 and 5"),
    "text": fields.String(required=True, description="Review text"),
    "upload_image": fields.List(fields.String, required=False, description="List of image URLs")
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
    @api.response(201, 'Review created successfully', review_response_model)
    @api.response(400, 'Invalid data or duplicate review')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place or user not found')
    #@api.marshal_with(review_response_model, code=201) 
    def post(self): 
        """Create a review""" 
        data = api.payload 
        current_user = get_jwt() 

        try:
            # Get place first
            place = facade.get_place(data["place_id"])
            if not place:
                return {'error': 'Place not found'}, 404

            # Owners cannot review their own place (optional)
            if str(place.owner_id) == str(current_user):
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
        except PermissionError as e:
            return {"error": str(e)}, 403  
            
"""Get, update, deleted review by id"""
@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review retrieved successfully', review_response_model)
    @api.response(404, 'Review not found')
    #@api.marshal_with(review_response_model, code=200)
    def get(self, review_id):
        """Get a single review by ID"""
        try:
            review = facade.get_review_by_id(review_id)
            return review.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 404

    @jwt_required()
    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully', review_response_model)
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review (owner only)"""
        data = api.payload or {}
        current_user = get_jwt()
        jwt_user_id = get_jwt_identity()
        
        is_admin = current_user.get('is_admin', False)

        try:
            review = facade.get_review_by_id(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
            
            if not is_admin and str(review.user.id) != str(jwt_user_id):
                return {"error": 'Unauthorised action'}, 403
            
            #update the review
            update = facade.update_review(review_id, data, jwt_user_id)
            return update.to_dict(), 200
        
        except PermissionError as e:
            return {"error": str(e)}, 403
        except ValueError as e:
            return {"error": str(e)}, 404

    @jwt_required()     
    @api.response(200, 'Review successfully deleted')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review (owner only)"""
        current_user = get_jwt()
        jwt_user_id = get_jwt_identity()

        is_admin = current_user.get('is_admin', False)

        try:
            # Fetch the review
            review = facade.get_review_by_id(review_id)
            if not review:
                return {"error": "Review not found"}, 404
            
            # Ownership check
            if not is_admin and str(review.user.id) != str(jwt_user_id):
                return {"error": "Unauthorized action."}, 403
            
            # Delete the review
            facade.delete_review(review_id, jwt_user_id)
            return {"message": "Review deleted successfully"}, 200

        except PermissionError as e:
            # In case the service layer also raises a permission error
            return {"error": str(e)}, 403
        except ValueError as e:
            # In case the review is not found
            return {"error": str(e)}, 404
        except Exception as e:
            # Catch any unexpected errors
            return {"error": str(e)}, 500
    
"""List all reviews of place"""
@api.route('/place/<string:place_id>')
class ReviewsByPlace(Resource):
    @api.response(200, 'List of reviews for the place', [review_response_model])
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """List all reviews for a specific place"""
        reviews = facade.get_reviews_for_place(place_id)
        # Return empty list if none
        return [r.to_dict() for r in reviews], 200

"""List review of user"""
@api.route('/user/<string:user_id>')
class ReviewsByUser(Resource):
    @api.response(200, 'List of reviews made by the user', [review_response_model])
    @api.response(404, 'User not found')
    def get(self, user_id):
        """List all reviews made by a specific user"""
        reviews = facade.get_reviews_by_user(user_id)
        # Return empty list if none
        return [r.to_dict() for r in reviews], 200