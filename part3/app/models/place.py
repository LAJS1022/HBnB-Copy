from app import db
from app.models.base_model import BaseModel

class Place(BaseModel):
    __tablename__ = 'places'

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    def __init__(self, name, description, owner, price=0.0, latitude=None, longitude=None):
        if not name:
            raise ValueError("Place must have a name")
        if price < 0:
            raise ValueError("Price must be non-negative")
        if latitude is not None and (latitude < -90 or latitude > 90):
            raise ValueError("Latitude must be between -90 and 90")
        if longitude is not None and (longitude < -180 or longitude > 180):
            raise ValueError("Longitude must be between -180 and 180")

        super().__init__()
        self.name = name
        self.description = description
        self.owner = owner
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.amenities = []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": {
                "id": self.owner.id,
                "first_name": self.owner.first_name,
                "last_name": self.owner.last_name,
                "email": self.owner.email,
            },
            "amenities": [a.to_dict() for a in self.amenities],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
