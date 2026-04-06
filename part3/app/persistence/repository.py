from app import db

class InMemoryRepository:
    def __init__(self):
        self.storage = {}

    def add(self, obj):
        self.storage[obj.id] = obj

    def get(self, obj_id):
        return self.storage.get(obj_id)

    def all(self):
        return list(self.storage.values())

    def delete(self, obj_id):
        if obj_id in self.storage:
            del self.storage[obj_id]

    def get_by_attribute(self, attr, value):
        return next(
            (obj for obj in self.storage.values()
             if getattr(obj, attr, None) == value),
            None
        )


class SQLAlchemyRepository:
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def all(self):
        return self.model.query.all()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr, value):
        return self.model.query.filter(
            getattr(self.model, attr) == value
        ).first()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
        return obj


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        from app.models.user import User
        super().__init__(User)

    def get_by_email(self, email):
        from app.models.user import User
        return User.query.filter_by(email=email).first()


class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        from app.models.place import Place
        super().__init__(Place)


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        from app.models.review import Review
        super().__init__(Review)


class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        from app.models.amenity import Amenity
        super().__init__(Amenity)
