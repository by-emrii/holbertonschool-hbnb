from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

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

# ============== Response enrichment helper function（using SQLAlchemy relationships） ==============
def _enrich_place_with_amenities(place, facade=facade):
    # Use relationship to get amenities directly
    amenities = []
    for amenity in place.amenities:
        amenities.append({
            'id': amenity.id,
            'name': amenity.name,
            'description': amenity.description,
        })

    # Use relationship to get owner directly
    owner = None
    if place.owner:
        owner = {
            'id': place.owner.id,
            'first_name': place.owner.first_name,
            'last_name': place.owner.last_name,
            'email': place.owner.email,
        }
    
    # Generate amenity_ids list for backward compatibility
    amenity_ids = [amenity.id for amenity in place.amenities]

    return {
        'id': place.id,
        'owner_id': place.owner_id,
        'title': place.title,
        'description': place.description or '',
        'price': place.price,
        'address': place.address,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'image_url': place.image_url,
        'amenity_ids': amenity_ids,
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
        current_user = get_jwt_identity()
        # place_data["owner_id"] = current_user
        try:
            place_data = api.payload
            place_data["owner_id"] = current_user
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
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """ Update place """
        data = api.payload or {}
        current_user = get_jwt()
        jwt_user_id = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        # user_id = current_user.get('id')

        try:
            # retrieve place and check ownership before update
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
            
            if not is_admin and str(place.owner_id) != str(jwt_user_id):
                return {'error': 'Unauthorized action'}, 403
            
            # if str(place.owner_id) != str(current_user):
            #     return {'error': 'Unauthorised action'}, 403
            
            # perform update
            updated_place = facade.update_place(place_id, data)
            return {
                'result': _enrich_place_with_amenities(updated_place),
                'message': 'Place updated successfully.'
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 404

    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, place_id):
        """
        Delete a place.
        Only the owner of the place or an admin can delete it.
        This will also delete all associated reviews and remove amenity associations.
        """
        current_user = get_jwt()
        jwt_user_id = get_jwt_identity()
        
        # Get admin status
        is_admin = current_user.get('is_admin', False)
        
        try:
            # Retrieve place to verify it exists
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
            
            # Check authorization: must be owner or admin
            if not is_admin and str(place.owner_id) != str(jwt_user_id):
                return {'error': 'Unauthorized action'}, 403
            
            # Perform deletion
            facade.delete_place(place_id)
            return {
                'message': 'Place deleted successfully.'
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 404

