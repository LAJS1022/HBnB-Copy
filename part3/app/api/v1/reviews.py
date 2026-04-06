from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.review import Review
from app.models.user import User
from app.models.place import Place
from app.services.facade import facade

ns = Namespace('reviews', description='Review operations')

review_model = ns.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True),
})

@ns.route('/')
class ReviewList(Resource):
    def get(self):
        return [r.to_dict() for r in facade.list_all() if isinstance(r, Review)]

    @jwt_required()
    @ns.expect(review_model)
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.json

        user = facade.get(data['user_id'])
        place = facade.get(data['place_id'])

        if not user or not isinstance(user, User):
            return {'error': 'User not found'}, 404
        if not place or not isinstance(place, Place):
            return {'error': 'Place not found'}, 404

        if user.id != current_user_id:
            return {'error': 'Unauthorized'}, 403

        if place.owner.id == current_user_id:
            return {'error': 'You cannot review your own place'}, 400

        duplicate = [r for r in facade.list_all()
                     if isinstance(r, Review)
                     and r.user.id == current_user_id
                     and r.place.id == place.id]
        if duplicate:
            return {'error': 'You have already reviewed this place'}, 400

        try:
            review = Review(data['text'], data['rating'], user, place)
        except ValueError as e:
            return {'error': str(e)}, 400

        facade.create(review)
        user.reviews.append(review)
        place.reviews.append(review)
        return review.to_dict(), 201

@ns.route('/<string:review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        review = facade.get(review_id)
        if not review or not isinstance(review, Review):
            return {'error': 'Review not found'}, 404
        return review.to_dict()

    @jwt_required()
    @ns.expect(review_model)
    def put(self, review_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        review = facade.get(review_id)
        if not review or not isinstance(review, Review):
            return {'error': 'Review not found'}, 404

        if review.user.id != current_user_id and not claims.get('is_admin'):
            return {'error': 'Unauthorized'}, 403

        data = request.json
        review.text = data.get('text', review.text)
        review.rating = data.get('rating', review.rating)
        review.update()
        return review.to_dict(), 200

    @jwt_required()
    def delete(self, review_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        review = facade.get(review_id)
        if not review or not isinstance(review, Review):
            return {'error': 'Review not found'}, 404

        if review.user.id != current_user_id and not claims.get('is_admin'):
            return {'error': 'Unauthorized'}, 403

        if review in review.user.reviews:
            review.user.reviews.remove(review)
        if review in review.place.reviews:
            review.place.reviews.remove(review)

        facade.delete(review_id)
        return {'message': 'Review deleted successfully'}, 200
