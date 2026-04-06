from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.review import Review
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
        return [r.to_dict() for r in facade.list_reviews()]

    @jwt_required()
    @ns.expect(review_model)
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.json

        user = facade.get_user(data['user_id'])
        place = facade.get_place(data['place_id'])

        if not user:
            return {'error': 'User not found'}, 404
        if not place:
            return {'error': 'Place not found'}, 404

        if user.id != current_user_id:
            return {'error': 'Unauthorized'}, 403

        if place.owner.id == current_user_id:
            return {'error': 'You cannot review your own place'}, 400

        duplicate = facade.review_repo.get_by_attribute('user_id', current_user_id)
        if duplicate and duplicate.place_id == place.id:
            return {'error': 'You have already reviewed this place'}, 400

        try:
            review = Review(data['text'], data['rating'], user, place)
        except ValueError as e:
            return {'error': str(e)}, 400

        facade.create_review(review)
        return review.to_dict(), 201

@ns.route('/<string:review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict()

    @jwt_required()
    @ns.expect(review_model)
    def put(self, review_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        review = facade.get_review(review_id)
        if not review:
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

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if review.user.id != current_user_id and not claims.get('is_admin'):
            return {'error': 'Unauthorized'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
