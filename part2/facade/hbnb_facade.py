from persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.repo = InMemoryRepository()

    def create(self, obj):
        self.repo.add(obj)
        return obj

    def get(self, obj_id):
        return self.repo.get(obj_id)

    def list_all(self):
        return self.repo.all()

    def delete(self, obj_id):
        self.repo.delete(obj_id)
