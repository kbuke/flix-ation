from config import db 
from sqlalchemy_serializer import SerializerMixin

class UserModel(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    img = db.Column(db.String, nullable=False)
    ac_type = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": ac_type
    }

class IndividualModel(UserModel):
    __tablename__ = "individuals"

    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)

    __mapper_args__ = {
        "polymorphic_identity": "individual"
    }

class CinemaModel(UserModel):
    __tablename__ = "cinemas"

    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    name = db.Column(db.String, nullable = False)
    address_1 = db.Column(db.String, nullable = False)
    address_2 = db.Column(db.String, nullable = True)
    country = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    town = db.Column(db.String, nullable=True)
    post_code = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "cinema"
    }