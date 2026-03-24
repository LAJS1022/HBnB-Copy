from business.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, user, place):
        super().__init__()
        if not text:
            raise ValueError("Review must have text")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        self.text = text
        self.rating = rating
        self.user = user     # relationship: Review belongs to User
        self.place = place   # relationship: Review belongs to Place

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user": {
                "id": self.user.id,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email,
            },
            "place_id": self.place.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
