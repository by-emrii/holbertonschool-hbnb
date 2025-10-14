from flask_restx import Namespace, Resource, fields
from app.services import HBnBFacade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'phone_number': fields.String(required=True, description='Phone number of the user'),
    'encrypted_password': fields.String(required=True, description='Enter password')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Invalid phone number')
    @api.response(400, 'Invalid password')
    def post(self):
        """Register a new user"""
        user_data = api.payload

         # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = HBnBFacade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = HBnBFacade.create_user(user_data)
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = HBnBFacade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.response(200, 'User details updated successfully!')
    @api.response(404, 'User not found')
    @api.response(404, 'Email already in use')
    @api.response(404, 'Invalid input')
    def put(self, user_id):
        """ Update user details """
        user_data = api.payload

        updated_user = HBnBFacade.update_user(user_id, user_data)
        if not updated_user:
            return {"error": "Update unsuccessful"}, 400
        return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email}, 200
