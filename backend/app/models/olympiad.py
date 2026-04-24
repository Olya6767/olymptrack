from ..database import db
from datetime import datetime


class Olympiad(db.Model):
    __tablename__ = "olympiads"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(100))
    deadline = db.Column(db.Date)
    status = db.Column(db.String(50), default="planned")  # planned, registered, submitted, won, lost
    result = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
