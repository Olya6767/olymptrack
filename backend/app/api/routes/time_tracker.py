from flask import Blueprint, request, jsonify
from ...database import db
from ...models.time_tracker import TimeEntry

bp = Blueprint("time_tracker", __name__, url_prefix="/api/time")


@bp.route("/", methods=["GET"])
def list_entries():
    user_id = request.args.get("user_id", type=int)
    query = TimeEntry.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    return jsonify([_serialize(e) for e in query.all()])


@bp.route("/", methods=["POST"])
def create_entry():
    data = request.get_json()
    entry = TimeEntry(
        user_id=data["user_id"],
        subject=data["subject"],
        date=data["date"],
        planned_minutes=data.get("planned_minutes", 0),
        actual_minutes=data.get("actual_minutes", 0),
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify(_serialize(entry)), 201


@bp.route("/<int:entry_id>", methods=["PUT"])
def update_entry(entry_id):
    entry = TimeEntry.query.get_or_404(entry_id)
    data = request.get_json()
    for field in ("planned_minutes", "actual_minutes", "subject", "date"):
        if field in data:
            setattr(entry, field, data[field])
    db.session.commit()
    return jsonify(_serialize(entry))


def _serialize(e):
    return {
        "id": e.id,
        "user_id": e.user_id,
        "subject": e.subject,
        "date": str(e.date),
        "planned_minutes": e.planned_minutes,
        "actual_minutes": e.actual_minutes,
    }
