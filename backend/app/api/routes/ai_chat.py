from flask import Blueprint, request, jsonify
from ...services.ai_service import get_ai_response

bp = Blueprint("ai_chat", __name__, url_prefix="/api/ai")


@bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_id = data.get("user_id")
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "message is required"}), 400
    reply = get_ai_response(user_id, message)
    return jsonify({"reply": reply})
