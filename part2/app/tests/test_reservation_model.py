#!/usr/bin/python3
"""
Run from project root with module flag:
python3 -m app.tests.test_reservation_model
"""
from app.models.reservation import Reservation
from datetime import datetime, timedelta

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

test_reservation_creation()
