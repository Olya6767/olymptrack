from flask import Blueprint, request, jsonify
from ...database import db
from ...models.olympiad import Olympiad

bp = Blueprint("olympiads", __name__, url_prefix="/api/olympiads")


@bp.route("/", methods=["GET"])
def list_olympiads():
    user_id = request.args.get("user_id", type=int)
    query = Olympiad.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    items = query.order_by(Olympiad.deadline).all()
    return jsonify([_serialize(o) for o in items])


@bp.route("/", methods=["POST"])
def create_olympiad():
    data = request.get_json()
    olympiad = Olympiad(
        user_id=data["user_id"],
        name=data["name"],
        subject=data.get("subject"),
        deadline=data.get("deadline"),
        status=data.get("status", "planned"),
        result=data.get("result"),
        notes=data.get("notes"),
    )
    db.session.add(olympiad)
    db.session.commit()
    return jsonify(_serialize(olympiad)), 201


@bp.route("/<int:olympiad_id>", methods=["PUT"])
def update_olympiad(olympiad_id):
    olympiad = Olympiad.query.get_or_404(olympiad_id)
    data = request.get_json()
    for field in ("name", "subject", "deadline", "status", "result", "notes"):
        if field in data:
            setattr(olympiad, field, data[field])
    db.session.commit()
    return jsonify(_serialize(olympiad))


@bp.route("/<int:olympiad_id>", methods=["DELETE"])
def delete_olympiad(olympiad_id):
    olympiad = Olympiad.query.get_or_404(olympiad_id)
    db.session.delete(olympiad)
    db.session.commit()
    return "", 204


def _serialize(o):
    return {
        "id": o.id,
        "user_id": o.user_id,
        "name": o.name,
        "subject": o.subject,
        "deadline": str(o.deadline) if o.deadline else None,
        "status": o.status,
        "result": o.result,
        "notes": o.notes,
    }
