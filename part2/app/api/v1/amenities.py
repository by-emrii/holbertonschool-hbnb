from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Define Namepsace for amenities operations
api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

# Define the Amenity model blueprint for validation and documentation
amenity_model = api.model('Amenity', {
    'id': fields.Integer(readonly=True, description='Amenity ID'),
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=False, description='Additional details of the amenity')
    })

# create root endpoint using Resource
@api.route('/')
class AmenityList(Resource):
    """ Collection level operations """
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """ Register a new amenity """
        # retrieve input data
        amenity_data = api.payload
        new_amenity = facade.create_amenity(amenity_data)
        if not new_amenity:
            return {'error': 'Invalid input data'}, 400
        return {'id': new_amenity.id, 'name': new_amenity.name, 'description': new_amenity.description}, 201

    @api.expect(amenity_model)
    @api.response(200, 'List of amenities retrieved successfully')
    @api.response(404, 'Amenities not found')
    def get(self):
        """ Retrieve a list of all amenities """
        all_amenities = facade.get_all_amenities()
        if not all_amenities:
            return {'error': 'Amenities not found'}, 404
        return [{'id': amenity.id, 'name': amenity.name, 'description': amenity.description} for amenity in all_amenities], 200
    
@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """ Individual level operations """
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """ Get amenity details by ID """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name, 'description': amenity.description}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """ Update an amenity's information """
        amenity_data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': updated_amenity.id, 'name': updated_amenity.name, 'description': updated_amenity.description}, 200
