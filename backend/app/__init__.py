from flask import Flask
from .database import db


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    if config:
        app.config.update(config)

    db.init_app(app)

    from .api.routes import olympiads, schedule, time_tracker, wishlist, mood, ai_chat
    app.register_blueprint(olympiads.bp)
    app.register_blueprint(schedule.bp)
    app.register_blueprint(time_tracker.bp)
    app.register_blueprint(wishlist.bp)
    app.register_blueprint(mood.bp)
    app.register_blueprint(ai_chat.bp)

    return app
