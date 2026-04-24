from flask import Blueprint, request, jsonify
from ...database import db
from ...models.mood import MoodEntry

bp = Blueprint("mood", __name__, url_prefix="/api/mood")


@bp.route("/", methods=["GET"])
def list_entries():
    user_id = request.args.get("user_id", type=int)
    query = MoodEntry.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    return jsonify([_serialize(e) for e in query.order_by(MoodEntry.date).all()])


@bp.route("/", methods=["POST"])
def create_entry():
    data = request.get_json()
    score = data["score"]
    if not (1 <= score <= 5):
        return jsonify({"error": "score must be between 1 and 5"}), 400
    entry = MoodEntry(
        user_id=data["user_id"],
        date=data["date"],
        score=score,
        note=data.get("note"),
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify(_serialize(entry)), 201


def _serialize(e):
    return {
        "id": e.id,
        "user_id": e.user_id,
        "date": str(e.date),
        "score": e.score,
        "note": e.note,
    }
