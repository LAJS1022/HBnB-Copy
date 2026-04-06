from app import bcrypt
import uuid
from datetime import datetime

class User:
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        if not email or "@" not in email:
            raise ValueError("Invalid email address")
        if not password:
            raise ValueError("Password is required")

        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        # Hash the password before storing
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Check if provided password matches the stored hash"""
        return bcrypt.check_password_hash(self.password, password)

    def update(self):
        self.updated_at = datetime.now()

    def to_dict(self):
        """Never expose the password"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
