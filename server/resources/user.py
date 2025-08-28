from config import db 

from models.user import UserModel, IndividualModel, CinemaModel

from flask_restful import Resource
from flask import session, make_response, request

class UserList(Resource):
    def post(self):
        json = request.get_json()

        # Validation for account types
        ac_type = json.get("ac_type")

        if ac_type == "individual":
            try:
                new_user = IndividualModel(
                    email = json.get("email"),
                    img = json.get("img"),
                    ac_type = ac_type,
                    username = json.get("username")
                )
                db.session.add(new_user)
                db.session.commit()
                return new_user.to_dict()
            except ValueError as e:
                return {"error": [str(e)]}
            
        elif ac_type == "cinema":
            try:
                new_user = CinemaModel(
                    email = json.get("email"),
                    img = json.get("img"),
                    ac_type = ac_type,
                    name = json.get("name"),
                    address_1 = json.get("address1"),
                    address_2 = json.get("address2"),
                    country = json.get("country"),
                    city = json.get("city"),
                    town = json.get("town"),
                    post_code = json.get("postCode")
                )
                db.session.add(new_user)
                db.session.commit()
                return new_user.to_dict()
            except ValueError as e:
                return {"error": [str(e)]}
            
        else:
            return {"error": "Account type must either be cinema or individual"}


