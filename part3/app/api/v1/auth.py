from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.services.facade import facade

ns = Namespace('auth', description='Authentication operations')

login_model = ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
})

@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        """Login and receive a JWT token"""
        data = request.json

        user = next(
            (u for u in facade.list_all()
             if isinstance(u, User) and u.email == data.get('email')),
            None
        )

        
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
