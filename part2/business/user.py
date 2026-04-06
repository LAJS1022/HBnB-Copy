from business.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password):
        super().__init__()
        if not email or "@" not in email:
            raise ValueError("Invalid email address")
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password   # stored, but not exposed
        self.places = []
        self.reviews = []

    def to_dict(self):
        """Return user data without password"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
