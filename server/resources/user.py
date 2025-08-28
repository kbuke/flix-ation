from config import db 

from models.user import UserModel, IndividualModel, CinemaModel

from flask_restful import Resource
from flask import session, make_response, request

import re

class UserList(Resource):
    def get(self):
        users = [user.to_dict() for user in UserModel.query.all()]
        return users 
    
    def post(self):
        json = request.get_json()

        # Validation for user emails
        user_email = json.get("email")

        all_emails = [user.email for user in UserModel.query.all()]
        print(all_emails)

        pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

        if pattern.match(user_email):

            if user_email in all_emails:
                return {"error": "This email is already reigistered"}, 409

        else:
            return{"error": "Please enter valid email"}
        
        # Validation for username
        selected_username = json.get("username")

        all_usernames = [user.username for user in UserModel.query.all()]

        if selected_username in all_usernames:
            return{"error": "Username already exists"}, 409

        # Validation for account types
        ac_type = json.get("ac_type")

        if ac_type == "individual":
            try:
                new_user = IndividualModel(
                    email = user_email,
                    img = json.get("img"),
                    ac_type = ac_type,
                    username = selected_username
                )
                db.session.add(new_user)
                db.session.commit()
                return new_user.to_dict()
            except ValueError as e:
                return {"error": [str(e)]}
            
        elif ac_type == "cinema":
            try:
                new_user = CinemaModel(
                    email = user_email,
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

class User(Resource):
    def get(self, id):
        user = UserModel.query.filter(UserModel.id==id).first()
        if user:
            return make_response(user.to_dict())
        else:
            return {"error": "User not found"}, 404
        
    def patch(self, id):
        data = request.get_json()

        user = UserModel.query.filter(UserModel.id==id).first()

        if user:
            try:
                for attr in data:
                    setattr(user, attr, data[attr])
                db.session.add(user)
                db.session.commit()
                return user.to_dict()
            except ValueError as e:
                return {"error": [str(e)]}
        else:
            return {"error": f"User {id} not found"}, 404
