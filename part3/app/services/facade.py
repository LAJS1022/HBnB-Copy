from app.persistence.repository import (
    UserRepository, PlaceRepository,
    ReviewRepository, AmenityRepository
)

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

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

    def create_place(self, obj):
        self.place_repo.add(obj)
        return obj

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def list_places(self):
        return self.place_repo.all()

    def update_place(self, place_id, data):
        return self.place_repo.update(place_id, data)

    def delete_place(self, place_id):
        self.place_repo.delete(place_id)

    def create_review(self, obj):
        self.review_repo.add(obj)
        return obj

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def list_reviews(self):
        return self.review_repo.all()

    def update_review(self, review_id, data):
        return self.review_repo.update(review_id, data)

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)

    def create_amenity(self, obj):
        self.amenity_repo.add(obj)
        return obj

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def list_amenities(self):
        return self.amenity_repo.all()

    def update_amenity(self, amenity_id, data):
        return self.amenity_repo.update(amenity_id, data)

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

facade = HBnBFacade()
