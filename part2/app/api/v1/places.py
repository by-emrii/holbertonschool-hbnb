from flask_restx import Namespace, Resource, fields
from app.services import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

# Create / Update 
place_create_model = api.model('PlaceCreate', {
    'user_id':     fields.String(required=True,  description='Owner user id'),
    'title':       fields.String(required=True,  description='Listing title'),
    'description': fields.String(required=False, description='Description'),
    'price':       fields.Float(required=True,   description='Price (e.g., per night)'),
    'address':     fields.String(required=False, description='Address'),
    'latitude':    fields.Float(required=True,   description='Latitude (-90..90)'),
    'longitude':   fields.Float(required=True,   description='Longitude (-180..180)'),
    'image_url':   fields.String(required=False, description='Cover image URL'),
    'amenity_ids': fields.List(fields.String, required=False, description='Amenity id list')
})

place_update_model = api.model('PlaceUpdate', {
    'title':       fields.String(required=False),
    'description': fields.String(required=False),
    'price':       fields.Float(required=False),
    'address':     fields.String(required=False),
    'latitude':    fields.Float(required=False),
    'longitude':   fields.Float(required=False),
    'image_url':   fields.String(required=False),
    'amenity_ids': fields.List(fields.Integer, required=False),
})

# Place response model
place_response = api.model('Place', {
    'id':          fields.String,
    'user_id':     fields.String,
    'title':       fields.String,
    'description': fields.String,
    'price':       fields.Float,
    'address':     fields.String,
    'latitude':    fields.Float,
    'longitude':   fields.Float,
    'image_url':   fields.String,
    'amenity_ids': fields.List(fields.Integer),
})

# Place Endpoints 
@api.route('/')
class PlaceList(Resource):
    @api.expect(place_create_model, validate=True)
    @api.marshal_with(place_response, code=201)
    def post(self):
        """ Create place """
        data = api.payload
        place = facade.create_place(data)
        return place, 201

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_response, code=200)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """ Get place by ID """
        place = facade.get_place(place_id)
        return place, 200

    @api.expect(place_update_model, validate=True)
    @api.marshal_with(place_response, code=200)
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """ Update place """
        data = api.payload or {}
        place = facade.update_place(place_id, data)
        return place, 200