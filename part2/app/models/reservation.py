from app.models.base_model import BaseModel
from datetime import datetime
import uuid

ALLOWED_STATUSES = ["pending", "confirmed", "cancelled", "completed"]
ALLOWED_PAYMENT_STATUSES = ["unpaid", "paid", "refunded"]

class Reservation(BaseModel):
    def __init__(self, user_id, place_id, start_date, end_date, price, status="pending", payment_status="unpaid", discount=None):
        super().__init__()  # this sets id, created_at, updated_at

        self.user_id = user_id
        self.place_id = place_id
        self.start_date = start_date
        self.end_date = end_date
        self.price = price
        self.discount = discount
        self.status = status
        self.payment_status = payment_status

    """ Getters and Setters """
    """ User_id """
    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        # check uuid formatting
        try:
            uuid.UUID(str(value))
        except ValueError:
            raise ValueError("Invalid user_id: must be a valid UUID string")
        self._user_id = str(value)

    """ Place_id """
    @property
    def place_id(self):
        return self._place_id

    @place_id.setter
    def place_id(self, value):
        try:
            uuid.UUID(str(value))
        except ValueError:
            raise ValueError("Invalid place_id: must be a valid UUID string")
        self._place_id = str(value)

    """ Start_date """
    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        # check if the value is a datetime obj
        if not isinstance(value, datetime):
            raise TypeError("Start date must be a datetime object")
        
        # makes sure start date isn't in the past
        if value < datetime.now():
            raise ValueError("Start date cannot be in the past")
        
        self._start_date = value

        if hasattr(self, "_end_date"):
            self.validate_dates()

    """ End_date """
    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        # check if the value is a datetime obj
        if not isinstance(value, datetime):
            raise TypeError("End date must be a datetime object")
        
        self._end_date = value
        if hasattr(self, "_start_date"):
            self.validate_dates()

    """ Price """
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        
        # if value was an int, convert to float for consistency
        value = float(value)
        
        if value < 0:
            raise ValueError("Price must be a positive number")
        
        self._price = value

    """ Discount """
    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        if value is None:
            self._discount = None
            return

        if not isinstance(value, (int, float)):
            raise TypeError("Discount must be a number")
        
        value = float(value)

        if value <= 0:
            raise ValueError("Discount must be a positive number")
        
        if hasattr(self, "_price") and value > self._price:
            raise ValueError("Discount cannot be more than price")
        
        self._discount = value

    """ Status """
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status: must be one of {ALLOWED_STATUSES}")
        self._status = value

    """ Payment Status """
    @property
    def payment_status(self):
        return self._payment_status

    @payment_status.setter
    def payment_status(self, value):
        if value not in ALLOWED_PAYMENT_STATUSES:
            raise ValueError(f"Invalid payment status: must be one of {ALLOWED_PAYMENT_STATUSES}")
        self._payment_status = value

    """ Helper to validate date relationship """
    def validate_dates(self):
        if self._end_date <= self._start_date:
            raise ValueError("End date must be after a start date")