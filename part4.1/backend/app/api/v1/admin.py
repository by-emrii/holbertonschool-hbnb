from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from flask import request
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

create_amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='Amenity ID'),
    'name': fields.String(required=True, description='Name of the amenity', min_length=1, max_length=255),
    'description': fields.String(required=False, description='Additional details of the amenity', max_length=255)
    })

update_amenity_model = api.model('Amenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity', min_length=1, max_length=255),
    'description': fields.String(description='Additional details of the amenity', max_length=255)
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
    @api.expect(user_create_model, validate=True)
    @api.response(201, 'Admin successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Invalid phone number')
    @api.response(400, 'Invalid password')
    @jwt_required()
    def post(self):
        # current_user = get_jwt()
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        # Logic to create a new user
        try:
            # user_data = api.payload
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
    @api.expect(admin_user_update_model, validate=True)
    @api.response(200, 'User details updated successfully!')
    @api.response(404, 'User not found')
    @api.response(404, 'Email already in use')
    @api.response(404, 'Invalid input')
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt()
        
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
    @api.expect(create_amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def post(self):
        current_user = get_jwt()
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
    @api.expect(update_amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt()
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

@api.route('/amenities/<amenity_id>')
class AdminAmenityDelete(Resource):
    @jwt_required()
    @api.response(200, 'Amenity successfully deleted')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        try:
            claims = get_jwt()
            if not claims.get('is_admin'):
                raise PermissionError('Admin privileges required')
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                raise ValueError('Amenity not found')
            facade.delete_amenity(amenity_id)
            return {'message': 'Amenity successfully deleted'}, 200
        except (PermissionError, ValueError) as e:
            error_message = str(e)
            if error_message.startswith('403'):
                return {'error': error_message}, 403    
            if error_message.startswith('404'):
                return {'error': error_message}, 404