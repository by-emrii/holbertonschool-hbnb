from flask_restx import Namespace, Resource, fields
# from app.services.facade import HBnBFacade

from app.services import facade   #  shared singleton

# Define Namepsace for amenities operations
api = Namespace('amenities', description='Amenity operations')

# facade = HBnBFacade()

# Define the Amenity model blueprint for validation and documentation
amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='Amenity ID'),
    'name': fields.String(required=True, description='Name of the amenity', min_length=1, max_length=50),
    'description': fields.String(required=False, description='Additional details of the amenity', max_length=100)
    })

# create root endpoint using Resource
@api.route('/')
class AmenityList(Resource):
    """ Collection level operations """
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """ Register a new amenity """
        # retrieve input data
        try:
            amenity_data = api.payload
            new_amenity = facade.create_amenity(amenity_data)
            return {'id': new_amenity.id, 'name': new_amenity.name, 'description': new_amenity.description}, 201
        # if not new_amenity:
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400
        

    @api.response(200, 'List of amenities retrieved successfully')
    @api.response(404, 'Amenities not found')
    def get(self):
        """ Retrieve a list of all amenities """
        try:
            all_amenities = facade.get_all_amenities()
            return [{'id': amenity.id, 'name': amenity.name, 'description': amenity.description} for amenity in all_amenities], 200
        except ValueError as e:
            return {'error': str(e)}, 404
            
    
@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """ Individual level operations """
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """ Get amenity details by ID """
        try:
            amenity = facade.get_amenity(amenity_id)
            return {'id': amenity.id,
                    'name': amenity.name, 
                    'description': amenity.description}, 200
        except (TypeError,ValueError) as e:
            return {'error': str(e)}, 404
            

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """ Update an amenity's information """
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
