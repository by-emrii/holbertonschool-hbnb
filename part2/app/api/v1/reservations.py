from flask_restx import Namespace, Resource, fields
from app.services import HBnBFacade

api = Namespace('reservations', description="Reservation operations")
facade = HBnBFacade() #ensures a single instance

# Main reservation model for creation (POST)
reservation_model = api.model('Reservation', {
    "user_id": fields.String(required=True, description= "ID of user making the reservation is required"),
    "place_id": fields.String(required=True, description="ID of the place being reserved is required"),
    "start_date": fields.String(required=True, description="Start date in ISO format(YYYY-MM-DD HH:MM:SS)"),
    "end_date": fields.String(required=True, description="Start date in ISO format(YYYY-MM-DD HH:MM:SS)"),
    "price": fields.Float(required=True, description="Total price of the reservation"),
    "discount": fields.Float(required=False, description="Discount amount"),
    "status": fields.String(required=False, description="Reservation status (pending, confirmed, cancelled, completed)"),
    "payment_status": fields.String(required=False, description="Payment status (unpaid, paid, refunded)")
})

# Reservation model for updates (PUT)
reservation_update_model = api.model('ReservationUpdate', {
    "start_date": fields.String(required=False, description="Start date in ISO format"),
    "end_date": fields.String(required=False, description="End date in ISO format"),
    "discount": fields.Float(required=False, description="Discount amount"),
    "status": fields.String(required=False, description="Reservation status"),
    "payment_status": fields.String(required=False, description="Payment status")
})

@api.route("/")
class ReservationList(Resource):
    @api.expect(reservation_model, validate=True)
    @api.response(201, "Reservation created successfully!")
    @api.response(400, "Invalid input data")
    def post(self):
        """ Create a new reservation """
        reservation_data = api.payload

        try:
            new_reservation = facade.create_reservation(reservation_data)
            return {
                "id": new_reservation.id,
                "user_id": new_reservation.user_id,
                "place_id": new_reservation.place_id,
                "start_date": new_reservation.start_date.isoformat(),
                "end_date": new_reservation.end_date.isoformat(),
                "price": new_reservation.price,
                "status": new_reservation.status,
                "payment_status": new_reservation.payment_status
            }, 201
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500

    @api.response(200, "All reservations retrieved successfully!")
    def get(self):
        """ Get all reservations """
        reservations = facade.get_all_reservations()
        if not reservations:
            # better to return an empty list than a message
            return [], 200
        result = [
            {
                "id": r.id,
                "user_id": r.user_id,
                "place_id": r.place_id,
                "start_date": r.start_date.isoformat(),
                "end_date": r.end_date.isoformat(),
                "price": r.price,
                "status": r.status,
                "payment_status": r.payment_status
            }
            # loop over iterable list of reservations
            for r in reservations
        ]
        return result

@api.route("/<reservation_id>")
class ReservationResource(Resource):
    @api.response(200, "Reservation retrieved successfully!")
    @api.response(403, "Reservation not found")
    def get(self, reservation_id):
        """ Get one reservation by ID """
        reservation = facade.get_reservation(reservation_id)
        if not reservation:
            return {"error": "Reservation not found"}, 404
        
        return {
            "id": reservation.id,
            "user_id": reservation.user_id,
            "place_id": reservation.place_id,
            "start_date": reservation.start_date.isoformat(),
            "end_date": reservation.end_date.isoformat(),
            "price": reservation.price,
            "status": reservation.status,
            "payment_status": reservation.payment_status
        }, 200

    @api.expect(reservation_update_model, validate=True)
    @api.response(200, "Reservation updated successfully!")
    @api.response(400, 'Invalid data or update failed')
    @api.response(404, 'Reservation not found')
    def put(self, reservation_id):
        """ Update an existing reservation """
        reservation_data = api.payload

        try:
            updated_reservation = facade.update_reservation(reservation_id, reservation_data)
            return {
                "id": updated_reservation.id,
                "user_id": updated_reservation.user_id,
                "place_id": updated_reservation.place_id,
                "start_date": updated_reservation.start_date.isoformat(),
                "end_date": updated_reservation.end_date.isoformat(),
                "price": updated_reservation.price,
                "discount": updated_reservation.discount,
                "status": updated_reservation.status,
                "payment_status": updated_reservation.payment_status
            }, 200
        except ValueError as e:
            # handle both not found and invalid field updates
            message = str(e)
            if message.startswith("404"):
                return {"error": "Reservation not found"}, 404
            return {"error": message}, 400
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500