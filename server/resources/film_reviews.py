from flask import session, make_response, request
from flask_restful import Resource

from config import db 

from models.film_reviews import ReviewModel

class FilmReviewList(Resource):
    def post(self):
        json = request.get_json()

        if json:
            try:
                new_review = ReviewModel(
                    rating = json.get("rating"),
                    review_title = json.get("reviewTitle"),
                    review = json.get("review"),
                    individual_id = json.get("userId"),
                    film_api_id = json.get("filmId")
                )
                db.session.add(new_review)
                db.session.commit()
                return make_response(new_review.to_dict(), 201)
            except ValueError as e:
                return {"error": [str(e)]}
        else:
            return {"error": "No data found"}, 404
        
class FilmReview(Resource):
    def delete(self, id):
        review = ReviewModel.query.filter(ReviewModel.id==id).first()
        if review:
            db.session.delete(review)
            db.session.commit()
            return {"message": f"Review {id} deleted"}, 201
        else:
            return {"error": f"Review {id} not found."}, 404