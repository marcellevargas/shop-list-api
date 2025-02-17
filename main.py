from flask import Flask
from config import Config
from database import db
from routes import graphql_server, graphql_playground

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.add_url_rule("/graphql", "graphql_playground", graphql_playground, methods=["GET"])
    app.add_url_rule("/graphql", "graphql_server", graphql_server, methods=["POST"])

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
