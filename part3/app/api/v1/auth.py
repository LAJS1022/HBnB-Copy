from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import facade

ns = Namespace('auth', description='Authentication operations')

login_model = ns.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        data = request.json

        user = facade.get_user_by_email(data.get('email'))

        if not user or not user.verify_password(data.get('password')):
            return {'error': 'Invalid email or password'}, 401

        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                'is_admin': user.is_admin,
                'email': user.email
            }
        )

        return {
            'access_token': access_token,
            'user_id': user.id,
            'is_admin': user.is_admin
        }, 200
