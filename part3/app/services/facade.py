from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create(self, obj):
        repo = self._get_repo(obj)
        repo.add(obj)
        return obj

    def get(self, obj_id):
        for repo in [self.user_repo, self.place_repo,
                     self.review_repo, self.amenity_repo]:
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

    def get_by_attribute(self, model_class, attr, value):
        repo = self._get_repo_by_class(model_class)
        return repo.get_by_attribute(attr, value)

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

    def _get_repo_by_class(self, model_class):
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
        return mapping.get(model_class, self.user_repo)

facade = HBnBFacade()
