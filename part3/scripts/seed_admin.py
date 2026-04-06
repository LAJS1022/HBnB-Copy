import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import create_app, db, bcrypt
from app.models.user import User
from app.models.amenity import Amenity

app = create_app('development')

with app.app_context():
    db.create_all()

    if not User.query.filter_by(email='admin@hbnb.io').first():
        admin = User(
            first_name='Admin',
            last_name='HBnB',
            email='admin@hbnb.io',
            password='admin1234',
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Admin created with id: {admin.id}")
    else:
        print("Admin already exists")

    amenities = ['WiFi', 'Swimming Pool', 'Air Conditioning']
    for name in amenities:
        if not Amenity.query.filter_by(name=name).first():
            amenity = Amenity(name=name)
            db.session.add(amenity)
            print(f"Amenity created: {name}")
        else:
            print(f"Amenity already exists: {name}")

    db.session.commit()
    print("Done!")
