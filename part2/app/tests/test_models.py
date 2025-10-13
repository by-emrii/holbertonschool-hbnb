#!/usr/bin/python3
"""
Run from project root with module flag:
python3 -m app.tests.test_models
"""

# from app.models.users import User
# from app.models.reviews import Review
# from app.models.reservation import Reservation

from app.models.amenity import Amenity
from app.models.place import Place


""" Testing the Amenities Class """
def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi", description="5G internet")
    assert amenity.name == "Wi-Fi"
    assert amenity.description == "5G internet"
    print("Amenity creation test passed!")


""" Testing the Place Class """
def test_place_creation():
    place = Place(
        user_id=1,
        title="Cozy Flat",
        description="Nice 2-bedroom flat near city center",
        price=240.0,
        address="888 Main St, Melbourne",
        latitude=-24.7241,
        longitude=124.6281,
        profile_img="https://example.com/image.jpg",
        amenity_ids=[1, 2, 2, 3]  #  test for removing duplicate ids
    )

    assert place.title == "Cozy Flat"
    assert place.price == 240.0
    assert len(place.amenity_ids) == 3   #  [1, 2, 3]
    assert 2 in place.amenity_ids

    print("Place creation test passed!")

test_amenity_creation()
test_place_creation()
