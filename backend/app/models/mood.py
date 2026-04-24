from ..database import db
from datetime import datetime


class MoodEntry(db.Model):
    __tablename__ = "mood_entries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    score = db.Column(db.Integer, nullable=False)  # 1-5
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
