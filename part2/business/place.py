from business.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, name, description, owner, price=0.0, latitude=None, longitude=None):
        super().__init__()
        if not name:
            raise ValueError("Place must have a name")
        if price < 0:
            raise ValueError("Price must be non-negative")
        if latitude is not None and (latitude < -90 or latitude > 90):
            raise ValueError("Latitude must be between -90 and 90")
        if longitude is not None and (longitude < -180 or longitude > 180):
            raise ValueError("Longitude must be between -180 and 180")

        self.name = name
        self.description = description
        self.owner = owner   # relationship: Place belongs to a User
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.amenities = []  # relationship: Place has Amenities

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
