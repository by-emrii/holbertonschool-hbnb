#!/usr/bin/python3
"""
Run from project root with module flag:
python3 -m app.tests.test_models
"""
# from app.models.places import Place
# from app.models.users import User
# from app.models.reviews import Review
# from app.models.reservation import Reservation
from app.models.amenity import Amenity

""" Testing the Amenities Class """
def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    print("Amenity creation test passed!")

test_amenity_creation()
