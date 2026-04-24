from ..database import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.BigInteger, unique=True, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    olympiads = db.relationship("Olympiad", backref="user", lazy=True)
    schedule_entries = db.relationship("ScheduleEntry", backref="user", lazy=True)
    time_entries = db.relationship("TimeEntry", backref="user", lazy=True)
    wishlist_items = db.relationship("WishlistItem", backref="user", lazy=True)
    mood_entries = db.relationship("MoodEntry", backref="user", lazy=True)
