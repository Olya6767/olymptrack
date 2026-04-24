from flask import Blueprint, request, jsonify
from ...database import db
from ...models.schedule import ScheduleEntry

bp = Blueprint("schedule", __name__, url_prefix="/api/schedule")


@bp.route("/", methods=["GET"])
def list_entries():
    user_id = request.args.get("user_id", type=int)
    query = ScheduleEntry.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    return jsonify([_serialize(e) for e in query.all()])


@bp.route("/", methods=["POST"])
def create_entry():
    data = request.get_json()
    entry = ScheduleEntry(
        user_id=data["user_id"],
        subject=data["subject"],
        day_of_week=data.get("day_of_week"),
        date=data.get("date"),
        time_start=data.get("time_start"),
        time_end=data.get("time_end"),
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify(_serialize(entry)), 201


@bp.route("/<int:entry_id>/skip", methods=["PATCH"])
def mark_skip(entry_id):
    entry = ScheduleEntry.query.get_or_404(entry_id)
    data = request.get_json()
    entry.skipped = data.get("skipped", True)
    entry.skip_reason = data.get("skip_reason")
    db.session.commit()
    return jsonify(_serialize(entry))


def _serialize(e):
    return {
        "id": e.id,
        "user_id": e.user_id,
        "subject": e.subject,
        "day_of_week": e.day_of_week,
        "date": str(e.date) if e.date else None,
        "time_start": str(e.time_start) if e.time_start else None,
        "time_end": str(e.time_end) if e.time_end else None,
        "skipped": e.skipped,
        "skip_reason": e.skip_reason,
    }
