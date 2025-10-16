from app.models.reservation import Reservation
from app.persistence.repository import InMemoryRepository


class ReservationService:
    def __init__(self):
        self.reservation_repo = InMemoryRepository()

    def create_reservation(self, reservation_data):
        """ Create a new reservation """
        # check for any missing data - user_id and place_id
        if "user_id" not in reservation_data or "place_id" not in reservation_data:
            raise ValueError("Missing required fields: user_id or place_id")

        reservation = Reservation(**reservation_data)
        self.reservation_repo.add(reservation)
        return reservation

    def get_reservation(self, reservation_id):
        """ Get one reservation by ID """
        return self.reservation_repo.get(reservation_id)

    def get_all_reservations(self):
        """ Get all reservations """
        return self.reservation_repo.get_all()

    def update_reservation(self, reservation_id, reservation_data):
        """ Update an existing reservation """
        reservation = self.reservation_repo.get(reservation_id)
        if not reservation:
            raise ValueError("404: Reservation not found")

        updatable_fields = {
            "start_date",
            "end_date",
            "price",
            "discount",
            "status",
            "payment_status"
        }

        for key, value in reservation_data.items():
            if key in updatable_fields and value is not None:
                setattr(reservation, key, value)

        return self.reservation_repo.update(reservation)
