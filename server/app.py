from config import app, api

from resources.user import UserList, User, IndividualList, Individual, CinemaList, Cinema

api.add_resource(UserList, "/users")
api.add_resource(User, "/users/<int:id>")
api.add_resource(IndividualList, "/individuals")
api.add_resource(Individual, "/individuals/<int:id>")
api.add_resource(CinemaList, "/cinemas")
api.add_resource(Cinema, "/cinemas/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)