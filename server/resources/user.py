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

        if not user:
            return {"error": f"User {id} not found"}, 404
        
        # username validation
        update_username = data.get("username")
            #-----filters all other users except the current one to ensure it does not notice the email or username already exists
        all_usernames = [user.username for user in IndividualModel.query.all() if user.id != id]
        if update_username and update_username in all_usernames:
            return {"error": f"Username {update_username} already exists."}, 409
        
        # email validation
        update_email = data.get("email")
        all_emails = [user.email for user in UserModel.query.all() if user.id != id]
        if update_email and update_email in all_emails:
            return{"error": f"Email address {update_email} already exists"}, 409
        
        try:
            for attr in data:
                setattr(user, attr, data[attr])
            db.session.add(user)
            db.session.commit()
            return make_response(user.to_dict())
        except ValueError as e:
            return {"error": [str(e)]}
    
    def delete(self, id):
        user = UserModel.query.filter(UserModel.id==id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"success": f"User {id} deleted"}, 200
        else:
            return {"error": f"User {id} not found"}, 404
        
class IndividualList(Resource):
    def get(self):
        individuals = [individual.to_dict() for individual in IndividualModel.query.all()]
        return individuals, 200
    
class Individual(Resource):
    def get(self, id):
        individual = IndividualModel.query.filter(IndividualModel.id==id).first()
        if individual:
            return individual.to_dict(), 200
        else:
            return {"error": f"Individual {id} not found"}, 404
        
class CinemaList(Resource):
    def get(self):
        cinemas = [cinema.to_dict() for cinema in CinemaModel.query.all()]
        return cinemas
        
        

