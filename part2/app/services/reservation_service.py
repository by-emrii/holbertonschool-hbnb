from datetime import datetime
from app.models.reservation import Reservation
from app.persistence.repository import InMemoryRepository

# define one global repo instance
reservation_repo = InMemoryRepository()

class ReservationService:
    def __init__(self):
        self.reservation_repo = reservation_repo

    def create_reservation(self, reservation_data):
        """ Create a new reservation """

        # Check for any missing data - user_id and place_id
        if "user_id" not in reservation_data or "place_id" not in reservation_data:
            raise ValueError("Missing required fields: user_id or place_id")

        # Convert start_date and end_date from ISO string to datetime object before creation
        reservation_data = reservation_data.copy() # to avoid mutating input
        reservation_data["start_date"] = datetime.fromisoformat(reservation_data["start_date"])
        reservation_data["end_date"] = datetime.fromisoformat(reservation_data["end_date"])

        # Create reservation object
        reservation = Reservation(**reservation_data)

        # Save to repository
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
            "discount",
            "status",
            "payment_status"
        }
        
        # Check for invalid fields
        invalid_fields = [key for key in reservation_data if key not in updatable_fields]
        if invalid_fields:
            raise ValueError(f"The following fields cannot be updated: {', '.join(invalid_fields)}")

        update_dict = {}

        for key, value in reservation_data.items():
            if key in updatable_fields and value is not None:
                # Convert ISO strings to datetime for date fields
                if key in ("start_date", "end_date"):
                    value = datetime.fromisoformat(value)
                setattr(reservation, key, value)
                update_dict[key] = value  # store the changes to pass to repo

        # Call repo update with obj_id and data dictionary
        self.reservation_repo.update(reservation, update_dict)
        return reservation