from flask import request
from flask_restx import Namespace, Resource, fields
from app.models.user import User
from app.services.facade import facade

ns = Namespace('users', description='User operations')

user_model = ns.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

@ns.route('/')
class UserList(Resource):
    def get(self):
        """Get all users - password never returned"""
        return [u.to_dict() for u in facade.list_all() if isinstance(u, User)]

    @ns.expect(user_model)
    def post(self):
        """Register a new user with hashed password"""
        data = request.json
        existing = [u for u in facade.list_all()
                    if isinstance(u, User) and u.email == data['email']]
        if existing:
            return {'error': 'Email already registered'}, 400

        try:
            user = User(
                data['first_name'],
                data['last_name'],
                data['email'],
                data['password'],  
                data.get('is_admin', False)
            )
            facade.create(user)
            return user.to_dict(), 201 
        except ValueError as e:
            return {'error': str(e)}, 400

@ns.route('/<string:user_id>')
class UserResource(Resource):
    def get(self, user_id):
        """Get user by ID - password never returned"""
        user = facade.get(user_id)
        if not user or not isinstance(user, User):
            return {'error': 'User not found'}, 404
        return user.to_dict() 

    @ns.expect(user_model)
    def put(self, user_id):
        user = facade.get(user_id)
        if not user or not isinstance(user, User):
            return {'error': 'User not found'}, 404

        data = request.json
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)

        if 'password' in data:
            from app import bcrypt
            user.password = bcrypt.generate_password_hash(
                data['password']).decode('utf-8')

        user.update()
        return user.to_dict(), 200
