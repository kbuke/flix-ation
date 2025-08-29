from sqlalchemy_serializer import SerializerMixin
from config import db 

class FaveCinemaModel(db.Model, SerializerMixin):
    __tablename__ = "fave_cinemas"

    id = db.Column(db.Integer, primary_key=True)
    individual_id = db.Column(db.Integer, db.ForeignKey("individuals.id", ondelete="CASCADE"))
    cinema_id = db.Column(db.Integer, db.ForeignKey("cinemas.id", ondelete="CASCADE"))