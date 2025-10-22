from flask_restx import Namespace, Resource, fields
from app.services import facade


api = Namespace('users', description='User operations')

# user = {
#     "user_id": "1",
#     "first_name": "Bob",
#     "last_name": "smith",
#     "email": "bobsmith@gmail.com",
#     "phone_number": "+61477448735",
#     "encrypted_password": "password"
# }

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'phone_number': fields.String(required=True, description='Phone number of the user'),
    'encrypted_password': fields.String(required=True, description='Enter password')
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
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response, code=201)
    # @api.response(201, 'User successfully created')
    # @api.response(400, 'Email already registered')
    # @api.response(400, 'Invalid input data')
    # @api.response(400, 'Invalid phone number')
    # @api.response(400, 'Invalid password')
    def post(self):
        """Register a new user"""
        try:
            user_data = api.payload

        #  # Simulate email uniqueness check (to be replaced by real validation with persistence)
        # existing_user = HBnBFacade.get_user_by_email(user_data['email'])
        # if existing_user:
        #     return {'error': 'Email already registered'}, 400

            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email, 'phone_number': new_user.phone_number}, 201
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400

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
        except ValueError as e:
            return {"error": str(e)}, 404

    @api.response(200, 'User details updated successfully!')
    @api.response(404, 'User not found')
    @api.response(404, 'Email already in use')
    @api.response(404, 'Invalid input')
    def put(self, user_id):
        """ Update user details """
        user_data = api.payload

        try:
            updated_user = facade.update_user(user_id, user_data)
            return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email, 'phone_number': updated_user.phone_number}, 200
        except ValueError as e:
            msg = str(e)
            if 'not found' in msg.lower():
                return {'error': msg}, 404
            return {"error": msg}, 400
