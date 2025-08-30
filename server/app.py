from config import app, api

from resources.user import UserList, User, IndividualList, Individual, CinemaList, Cinema
from resources.fave_cinemas import FaveCinemaList, FaveCinema
from resources.film_api import Film, FilmGenres
from resources.film_reviews import FilmReviewList, FilmReview

api.add_resource(UserList, "/users")
api.add_resource(User, "/users/<int:id>")
api.add_resource(IndividualList, "/individuals")
api.add_resource(Individual, "/individuals/<int:id>")
api.add_resource(CinemaList, "/cinemas")
api.add_resource(Cinema, "/cinemas/<int:id>")

api.add_resource(FaveCinemaList, "/favecinemas")
api.add_resource(FaveCinema, "/favecinemas/<int:id>")

api.add_resource(Film, "/movies/<film_id>")
api.add_resource(FilmGenres, "/genres")

api.add_resource(FilmReviewList, "/reviews")
api.add_resource(FilmReview, "/reviews/<int:id>")


if __name__ == "__main__":
    app.run(port=5555, debug=True)