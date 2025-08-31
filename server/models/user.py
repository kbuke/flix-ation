from config import db 
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates


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

    # Set up relations
    fave_cinemas = db.relationship("CinemaModel", back_populates="users_fave", secondary="fave_cinemas")
    reviews = db.relationship("ReviewModel", back_populates="individual", cascade="all, delete-orphan")

    serialize_rules = (
        "-fave_cinemas.users_fave",
        "-fave_cinemas.ac_type",
        "-fave_cinemas.address_1",
        "-fave_cinemas.address_2",
        "-fave_cinemas.city",
        "-fave_cinemas.country",
        "-fave_cinemas.email",
        "-fave_cinemas.post_code",
        "-fave_cinemas.town",

        "-reviews.individual",
    )

    __mapper_args__ = {
        "polymorphic_identity": "individual"
    }

    # Add property for reviews
    @property
    def serialized_reviews(self):
        reviews_data = []
        for r in self.reviews or []:
            review_dict = r.to_dict()
            review_dict["film"] = r.film_details
            reviews_data.append(review_dict)
        return reviews_data
    
    # Add property for watchlist


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

    users_fave = db.relationship("IndividualModel", back_populates="fave_cinemas", secondary="fave_cinemas")
    showings = db.relationship("CinemaShowingModel", back_populates="cinema", cascade="all, delete-orphan")

    serialize_rules = (
        "-users_fave.fave_cinemas",
        "-users_fave.email",
        "-users_fave.ac_type",
    )

    __mapper_args__ = {
        "polymorphic_identity": "cinema"
    }

    @property
    def serialized_screenings(self):
        screening_data = []
        for r in self.showings or []:
            screening_dict = r.to_dict()
            screening_dict["film"] = r.film_details
            screening_data.append(screening_dict)
        return screening_data