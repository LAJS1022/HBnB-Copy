from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.models.amenity import Amenity
from app.services.facade import facade

ns = Namespace('amenities', description='Amenity operations')

amenity_model = ns.model('Amenity', {
    'name': fields.String(required=True),
})

@ns.route('/')
class AmenityList(Resource):
    def get(self):
        return [a.to_dict() for a in facade.list_all() if isinstance(a, Amenity)]

    @jwt_required()
    @ns.expect(amenity_model)
    def post(self):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin access required'}, 403

        data = request.json
        try:
            amenity = Amenity(data['name'])
        except ValueError as e:
            return {'error': str(e)}, 400

        facade.create(amenity)
        return amenity.to_dict(), 201

@ns.route('/<string:amenity_id>')
class AmenityResource(Resource):
    def get(self, amenity_id):
        amenity = facade.get(amenity_id)
        if not amenity or not isinstance(amenity, Amenity):
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict()

    @jwt_required()
    @ns.expect(amenity_model)
    def put(self, amenity_id):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin access required'}, 403

        amenity = facade.get(amenity_id)
        if not amenity or not isinstance(amenity, Amenity):
            return {'error': 'Amenity not found'}, 404

        data = request.json
        amenity.name = data.get('name', amenity.name)
        amenity.update()
        return amenity.to_dict(), 200
