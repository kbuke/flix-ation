from config import app, api

from resources.user import UserList

api.add_resource(UserList, "/users")

if __name__ == "__main__":
    app.run(port=5555, debug=True)