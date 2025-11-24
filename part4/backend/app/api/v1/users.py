from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')


# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'phone_number': fields.String(required=False, description='Phone number of the user'),
    'password': fields.String(required=True, description='Enter password')
})

# Define the response for user model without pwd
user_response = api.model('User',{
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'phone_number': fields.String,
    'profile_img': fields.String,
    'is_admin': fields.Boolean,
})

@api.route('/')
class UserList(Resource):
    # @api.expect(user_model, validate=True) # GET method doesnt need it
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Invalid phone number')
    @api.response(400, 'Invalid password')

    # Get all users
    def get(self):
        users = facade.get_all_users()
        if not users:
            return [], 200
        result = [
            {
            'id': u.id,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
            'phone_number': u.phone_number,
            'profile_img': u.profile_img,
            'is_admin': u.is_admin
            }
            for u in users
        ]
        return result

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        try:
            user = facade.get_user(user_id)
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone_number': user.phone_number
            }, 200
        except (TypeError, ValueError) as e:
            return {"error": str(e)}, 404
