from ..database import db
from datetime import datetime


class WishlistItem(db.Model):
    __tablename__ = "wishlist_items"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default="idea")  # idea, in_progress, done, dropped
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
