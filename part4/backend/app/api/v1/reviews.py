from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace("reviews", description="Review operations")


review_create_model = api.model('ReviewCreate', {
    "place_id": fields.String(required=True, description="ID of the place being reviewed"),
    "rating": fields.Integer(required=True, min=1, max=5, description="Rating between 1 and 5"),
    "text": fields.String(required=True, description="Review text"),
})


review_update_model = api.model('ReviewUpdate', {
    "rating": fields.Integer(required=True, min=1, max=5),
    "text": fields.String(required=True, max_length=300),
})


review_response_model = api.model('Review', {
    "id": fields.String,
    "user_id": fields.String,
    "place_id": fields.String,
    "rating": fields.Integer,
    "text": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String,
})

"""Create a review for a place / List all reviews in database"""
@api.route('/')
class ReviewsList(Resource):
    @api.doc(security=None)
    @api.response(200, 'List of reviews made by the user', [review_response_model])
    def get(self):
        """List all reviews made by a specific user"""
        reviews = facade.get_all_reviews()

        reviews = [r for r in reviews if r.to_dict().get('place') is not None]

        return [r.to_dict() for r in reviews], 200

    """Create a review for a place"""
    @jwt_required() 
    @api.expect(review_create_model, validate=True) 
    @api.response(201, 'Review created successfully', review_response_model)
    @api.response(400, 'Invalid data or duplicate review')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place or user not found')
    def post(self): 
        """Create a review""" 
        data = api.payload 
        current_user = get_jwt_identity() 

        try:
            place = facade.get_place(data["place_id"])
            if not place:
                return {'error': 'Place not found'}, 404

            if str(place.owner_id) == str(current_user):
                return {'error': "You cannot review your own place."}, 400
            
            if facade.user_already_reviewed(place.id, current_user):
                return {'error': "You have already reviewed this place."}, 400

            user = facade.get_user(current_user)
            if not user:
                return {'error': 'User not found'}, 404

            review = facade.create_review({
                "user": user,
                "place": place,
                "rating": data["rating"],
                "text": data["text"],
            })

            return {
                "review": review.to_dict(),
                "message": "Review created successfully"
            }, 201

        except ValueError as e:
            return {"error": str(e)}, 400
        except PermissionError as e:
            return {"error": str(e)}, 403  
            
"""Get, update, deleted review by review_id"""
@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.doc(security=None)
    @api.response(200, 'Review retrieved successfully', review_response_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get a single review by ID"""

        try:
            review = facade.get_review_by_id(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
   
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
            
            update = facade.update_review(review_id, data, jwt_user_id, is_admin)
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
            review = facade.get_review_by_id(review_id)
            if not review:
                return {"error": "Review not found"}, 404
            
            if not is_admin and str(review.user.id) != str(jwt_user_id):
                return {"error": "Unauthorized action."}, 403
            
            facade.delete_review(review_id, jwt_user_id, is_admin)
            return {"message": "Review deleted successfully"}, 200

        except PermissionError as e:
            return {"error": str(e)}, 403
        except ValueError as e:
            return {"error": str(e)}, 404
        except Exception as e:
            return {"error": str(e)}, 500
    
"""List all reviews of place"""
@api.route('/place/<string:place_id>')
class ReviewsByPlace(Resource):
    @api.response(200, 'List of reviews for the place', [review_response_model])
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """List all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        reviews = facade.get_reviews_for_place(place_id)

        reviews = [r for r in reviews if r.to_dict().get('place') is not None]

        return [r.to_dict() for r in reviews], 200
