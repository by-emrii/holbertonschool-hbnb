from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Create / Update 
place_create_model = api.model('PlaceCreate', {
    'owner_id':     fields.String(required=True,  description='Owner id'),
    'title':       fields.String(required=True,  description='Listing title'),
    'description': fields.String(required=False, description='Description'),
    'price':       fields.Float(required=True,   description='Price (e.g., per night)'),
    'address':     fields.String(required=False, description='Address'),
    'latitude':    fields.Float(required=True,   description='Latitude (-90..90)'),
    'longitude':   fields.Float(required=True,   description='Longitude (-180..180)'),
    'image_url':   fields.String(required=False, description='Cover image URL'),
    'amenity_ids': fields.List(fields.String, required=False, description='Amenity id list(str)')
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

# Place response model
place_response = api.model('Place', {
    'id':          fields.String,
    'owner_id':     fields.String,
    'title':       fields.String,
    'description': fields.String,
    'price':       fields.Float,
    'address':     fields.String,
    'latitude':    fields.Float,
    'longitude':   fields.Float,
    'image_url':   fields.String,
    'amenity_ids': fields.List(fields.String),
})

# ============== Response enrichment helper function（same as part2, manually serialize） ==============
def _enrich_place_with_amenities(place, facade=facade):
    amenities = []
    for amenity_id in getattr(place, 'amenity_ids', []) or []:
        try:
            amenity = facade.get_amenity(amenity_id)
            amenities.append({
                'id': amenity.id,
                'name': getattr(amenity, 'name', None),
                'description': getattr(amenity, 'description', None),
            })
        except Exception:
            continue
    owner = None
    owner_id = getattr(place, 'owner_id', None)
    if owner_id:
        try:
            user = facade.get_user(owner_id)
            owner = {
                'id': user.id,
                'first_name': getattr(user, 'first_name', None),
                'last_name': getattr(user, 'last_name', None),
                'email': getattr(user, 'email', None),
            }
        except Exception:
            owner = None
    return {
        'id': place.id,
        'owner_id': getattr(place, 'owner_id', None),
        'title': place.title,
        'description': getattr(place, 'description', None),
        'price': place.price,
        'address': getattr(place, 'address', None),
        'latitude': place.latitude,
        'longitude': place.longitude,
        'image_url': getattr(place, 'image_url', None),
        'amenity_ids': list(getattr(place, 'amenity_ids', []) or []),
        'amenities': amenities,
        'owner': owner,
    }

# === Place Endpoints (remove marshal_with, directly jsonify data) ===
@api.route('/')
class PlaceList(Resource):
    @api.expect(place_create_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input')
    @api.response(403, 'Unauthorised action')
    @jwt_required()
    def post(self):
        place_data = api.payload
        current_user = get_jwt_identity()
        if 'owner_id' in place_data and place_data['owner_id'] != current_user:
            return {'error': 'Unauthorised action'}, 403
        try:
            place = facade.create_place(place_data)
            return {
                'result': _enrich_place_with_amenities(place),
                'message': 'Place successfully created.'
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of all places retrieved successfully')
    @api.response(404, 'No places found')
    def get(self):
        try:
            places = facade.list_places()
            enriched = [_enrich_place_with_amenities(p) for p in places]
            return {
                'result': enriched,
                'message': 'List of all places retrieved successfully.'
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 404

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    @api.doc(description="Get place by ID")
    def get(self, place_id):
        try:
            place = facade.get_place(place_id)
            return {
                'result': _enrich_place_with_amenities(place),
                'message': 'Place details retrieved successfully.'
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 404

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        try:
            data = api.payload or {}
            place = facade.update_place(place_id, data)
            return {
                'result': _enrich_place_with_amenities(place),
                'message': 'Place updated successfully.'
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 404
