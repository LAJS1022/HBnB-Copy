from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity
from app.services.facade import facade

ns = Namespace('places', description='Place operations')

place_model = ns.model('Place', {
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'owner_id': fields.String(required=True),
    'price': fields.Float(required=False),
    'latitude': fields.Float(required=False),
    'longitude': fields.Float(required=False),
    'amenity_ids': fields.List(fields.String, required=False),
})

@ns.route('/')
class PlaceList(Resource):
    def get(self):
        return [p.to_dict() for p in facade.list_all() if isinstance(p, Place)]

    @jwt_required()
    @ns.expect(place_model)
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.json

        owner = facade.get(data['owner_id'])
        if not owner or not isinstance(owner, User):
            return {'error': 'Owner not found'}, 404

        if owner.id != current_user_id:
            return {'error': 'Unauthorized'}, 403

        try:
            place = Place(
                data['name'],
                data['description'],
                owner,
                data.get('price', 0.0),
                data.get('latitude'),
                data.get('longitude'),
            )
        except ValueError as e:
            return {'error': str(e)}, 400

        for a_id in data.get('amenity_ids', []):
            amenity = facade.get(a_id)
            if amenity and isinstance(amenity, Amenity):
                place.amenities.append(amenity)

        facade.create(place)
        return place.to_dict(), 201

@ns.route('/<string:place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        place = facade.get(place_id)
        if not place or not isinstance(place, Place):
            return {'error': 'Place not found'}, 404
        return place.to_dict()

    @jwt_required()
    @ns.expect(place_model)
    def put(self, place_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        place = facade.get(place_id)
        if not place or not isinstance(place, Place):
            return {'error': 'Place not found'}, 404

        if place.owner.id != current_user_id and not claims.get('is_admin'):
            return {'error': 'Unauthorized'}, 403

        data = request.json
        place.name = data.get('name', place.name)
        place.description = data.get('description', place.description)
        place.price = data.get('price', place.price)
        place.latitude = data.get('latitude', place.latitude)
        place.longitude = data.get('longitude', place.longitude)

        amenity_ids = data.get('amenity_ids')
        if amenity_ids is not None:
            place.amenities = []
            for a_id in amenity_ids:
                amenity = facade.get(a_id)
                if amenity and isinstance(amenity, Amenity):
                    place.amenities.append(amenity)

        place.update()
        return place.to_dict(), 200

    @jwt_required()
    def delete(self, place_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        place = facade.get(place_id)
        if not place or not isinstance(place, Place):
            return {'error': 'Place not found'}, 404

        if place.owner.id != current_user_id and not claims.get('is_admin'):
            return {'error': 'Unauthorized'}, 403

        facade.delete(place_id)
        return {'message': 'Place deleted successfully'}, 200
