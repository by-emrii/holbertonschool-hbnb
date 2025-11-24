from flask_restx import Namespace, Resource, fields
# from app.services.facade import HBnBFacade
from app.services import facade # shared singleton

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
