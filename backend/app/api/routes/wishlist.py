from flask import Blueprint, request, jsonify
from ...database import db
from ...models.wishlist import WishlistItem

bp = Blueprint("wishlist", __name__, url_prefix="/api/wishlist")


@bp.route("/", methods=["GET"])
def list_items():
    user_id = request.args.get("user_id", type=int)
    query = WishlistItem.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    return jsonify([_serialize(i) for i in query.all()])


@bp.route("/", methods=["POST"])
def create_item():
    data = request.get_json()
    item = WishlistItem(
        user_id=data["user_id"],
        title=data["title"],
        description=data.get("description"),
        status=data.get("status", "idea"),
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(_serialize(item)), 201


@bp.route("/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = WishlistItem.query.get_or_404(item_id)
    data = request.get_json()
    for field in ("title", "description", "status"):
        if field in data:
            setattr(item, field, data[field])
    db.session.commit()
    return jsonify(_serialize(item))


def _serialize(i):
    return {
        "id": i.id,
        "user_id": i.user_id,
        "title": i.title,
        "description": i.description,
        "status": i.status,
    }
