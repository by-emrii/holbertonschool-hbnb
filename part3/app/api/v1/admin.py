from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from json import request
from app.services import facade

api = Namespace('admin', description='Admin operations')

# Define the user model for input validation and documentation
admin_user_update_model = api.model('AdminUpdateUser', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'phone_number': fields.String(description='Phone number of the user'),
    'password': fields.String(description='Enter password'),
    'is_admin': fields.Boolean(description='User role')
})

user_create_model = api.model('CreateUser', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'phone_number': fields.String(required=False, description='Phone number of the user'),
    'password': fields.String(required=True, description='Enter password')
})

amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='Amenity ID'),
    'name': fields.String(required=True, description='Name of the amenity', min_length=1, max_length=50),
    'description': fields.String(required=False, description='Additional details of the amenity', max_length=100)
    })


place_update_model = api.model('PlaceUpdate', {
    'title':       fields.String(required=False),
    'description': fields.String(required=False),
    'price':       fields.Float(required=False),
    'address':     fields.String(required=False),
    'latitude':    fields.Float(required=False),
    'longitude':   fields.Float(required=False),
    'image_url':   fields.String(required=False),
    'amenity_ids': fields.List(fields.String, required=False),
})


# Administrators can create new users. The email must be unique.
@api.route('/users/')
class AdminUserCreate(Resource):
    # @api.expect(user_create_model, validate=True)
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        # Logic to create a new user
        try:
            user_data = api.payload
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'message': "User registered sucessfully"
                }, 201
        except (TypeError,ValueError) as e:
            return {"error": str(e)}, 400


# Administrators can modify any user
@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        
        # If 'is_admin' is part of the identity payload
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        if email:
            # Check if email is already in use
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        # Logic to update user details, including email and password
        try:
            updated_user = facade.update_user(user_id, data)
            return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email, 'phone_number': updated_user.phone_number}, 200
        except (TypeError, ValueError) as e:
            msg = str(e)
            if 'not found' in msg.lower():
                return {'error': msg}, 404
            return {"error": msg}, 400


# Can add amenity to all places
@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Logic to create a new amenity
        try:
            amenity_data = api.payload
            new_amenity = facade.create_amenity(amenity_data)
            return {'id': new_amenity.id, 'name': new_amenity.name, 'description': new_amenity.description}, 201
        # if not new_amenity:
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400


# Can update amenity to all places
@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Logic to update an amenity
        try:
            amenity_data = api.payload
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name,
                'description': updated_amenity.description}, 200
        except (TypeError, ValueError) as e:
            error_message = str(e)
            if error_message.startswith('400'):
                return {'error':error_message}, 400
            elif error_message.startswith('404'):
                return {'error':error_message}, 404
            else:
                return {'error': 'An unexpected error occurred'}, 500


# Allow Admins to Bypass Ownership Restrictions
@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        # Logic to update the place
        data = api.payload or {}
        current_user = get_jwt_identity()
        # retrieve place
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        try:
            update_place = facade.update_place(place_id, data)
            if update_place.owner_id != current_user:
                return {'error': 'Unauthorised action'}, 403
            return update_place, 200
        except ValueError as e:
            return {"error:", str(e)}, 404