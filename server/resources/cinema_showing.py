from flask import session, make_response, request
from flask_restful import Resource
from config import db 
from models.cinema_showing import CinemaShowingModel
from datetime import datetime

class CinemaShowingList(Resource):
    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {"error": "Failed to load json"}, 404

        # Parse and validate input
        try:
            show_date = datetime.strptime(json_data.get("showDate"), "%Y-%m-%d").date()
            start_time = datetime.strptime(json_data.get("startTime"), "%H:%M").time()
            screen = json_data.get("screen")
            cinema_id = json_data.get("cinemaId")
            film_api_id = json_data.get("filmId")

            if not all([show_date, start_time, screen, cinema_id, film_api_id]):
                return {"error": "Missing required fields"}, 400

        except ValueError as e:
            return {"error": f"Invalid date or time format: {str(e)}"}, 400

        # Create a temporary showing object to calculate end_time
        temp_showing = CinemaShowingModel(
            show_date=show_date,
            start_time=start_time,
            screen=screen,
            cinema_id=cinema_id,
            film_api_id=film_api_id
        )
        end_time = temp_showing.calculate_end_time()

        # Fetch existing showings for that screen on the same date
        existing_showings = CinemaShowingModel.query.filter_by(
            show_date=show_date,
            screen=screen
        ).all()

        # Check for overlapping times
        for s in existing_showings:
            if (start_time < s.end_time) and (end_time > s.start_time):
                return {
                    "error": f"Screen {screen} already has a showing from {s.start_time.strftime('%H:%M')} to {s.end_time.strftime('%H:%M')}"
                }, 400

        # No conflicts, create the new showing
        new_showing = CinemaShowingModel(
            show_date=show_date,
            start_time=start_time,
            end_time=end_time,
            screen=screen,
            cinema_id=cinema_id,
            film_api_id=film_api_id
        )

        db.session.add(new_showing)
        db.session.commit()

        return new_showing.to_dict(), 201


class CinemaShowing(Resource):
    def delete(self, id):
        showing = CinemaShowingModel.query.filter(CinemaShowingModel.id==id).first()
        if showing:
            db.session.delete(showing)
            db.session.commit()
            return {"message": f"Showing {id} deleted"}, 201
        else:
            return {"error": f"Showing {id} not found"}, 404