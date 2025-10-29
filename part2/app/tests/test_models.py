#!/usr/bin/python3
"""
Run from project root with module flag:
python3 -m app.tests.test_models
"""


import pytest
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.reservation import Reservation
from datetime import datetime, timedelta
from app.models.review import Review


""" Testing the User Class """
def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com", phone_number="+6112345678", encrypted_password="Testp@ssword1?")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Default value
    assert user.phone_number == "+6112345678"
    assert user.encrypted_password == "Testp@ssword1?"
    print("User creation test passed!")


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
        image_url="https://example.com/image.jpg",
        amenity_ids=[1, 2, 2, 3]  #  test for removing duplicate ids
    )

    assert place.title == "Cozy Flat"
    assert place.price == 240.0
    assert len(place.amenity_ids) == 3   #  [1, 2, 3]
    assert 2 in place.amenity_ids

    print("Place creation test passed!")

""" Test Reservation class"""
def test_reservation_creation():
    # create start and end dates
    start = datetime.now() + timedelta(days=1) # tomorrow
    end = start + timedelta(days=5) # 5 days later

    # create reservation
    reservation = Reservation(
        user_id="1",
        place_id="1",
        start_date= start,
        end_date= end,
        price=500,
        discount=50,
        status="pending",
        payment_status="unpaid"
    )

    assert reservation.user_id == "1"
    assert reservation.place_id == "1"
    assert reservation.start_date == start
    assert reservation.end_date == end
    assert reservation.price == 500
    assert reservation.discount == 50
    assert reservation.status == "pending"
    assert reservation.payment_status == "unpaid"

    print("Reservation creation test passed!")

""" Test Review Class """
def test_review_creation():
    user = User(first_name="John", last_name="Doe", email="john@example.com", phone_number="+6112345678", encrypted_password="pass123")
    place = Place(
        user_id=user.id,
        title="Test Place",
        description="Nice place",
        price=100.0,
        address="123 Test St",
        latitude=0.0,
        longitude=0.0,
        image_url="https://example.com/place.jpg",
        amenity_ids=[]
    )
    review = Review(
        user=user,
        place=place,
        rating=4,
        text="Great experience!",
        upload_image=["https://example.com/review.jpg"]
    )
    assert review.user == user
    assert review.place == place
    assert review.rating == 4
    assert review.text == "Great experience!"
    assert review.upload_image == ["https://example.com/review.jpg"]
    
    print("Review creation test passed!")


test_user_creation()
test_amenity_creation()
test_place_creation()
test_reservation_creation()
test_review_creation()