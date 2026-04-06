from app.persistence.repository import InMemoryRepository, UserRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, obj):
        self.user_repo.add(obj)
        return obj

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_email(email)

    def list_users(self):
        return self.user_repo.all()

    def update_user(self, user_id, data):
        return self.user_repo.update(user_id, data)

    def create(self, obj):
        repo = self._get_repo(obj)
        repo.add(obj)
        return obj

    def get(self, obj_id):
        obj = self.user_repo.get(obj_id)
        if obj:
            return obj
        for repo in [self.place_repo, self.review_repo, self.amenity_repo]:
            obj = repo.get(obj_id)
            if obj:
                return obj
        return None

    def list_all(self):
        return (
            self.user_repo.all() +
            self.place_repo.all() +
            self.review_repo.all() +
            self.amenity_repo.all()
        )

    def delete(self, obj_id):
        for repo in [self.user_repo, self.place_repo,
                     self.review_repo, self.amenity_repo]:
            obj = repo.get(obj_id)
            if obj:
                repo.delete(obj_id)
                return

    def _get_repo(self, obj):
        from app.models.user import User
        from app.models.place import Place
        from app.models.review import Review
        from app.models.amenity import Amenity

        mapping = {
            User: self.user_repo,
            Place: self.place_repo,
            Review: self.review_repo,
            Amenity: self.amenity_repo,
        }
        return mapping.get(type(obj), self.user_repo)

facade = HBnBFacade()
