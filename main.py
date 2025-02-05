import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  done = db.Column(db.Boolean, default=False)

def todo_to_dict(todo):
  return {
    "id": todo.id,
    "title": todo.title,
    "done": todo.done
  }

@app.route("/todos", methods=["POST"])
def create_todo():
  data = request.json
  new_todo = Todo(title=data["title"], done=data.get("done", False))
  db.session.add(new_todo)
  db.session.commit()
  return jsonify(todo_to_dict(new_todo)), 201

@app.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo_to_dict(todo) for todo in todos])

@app.route("/todos/<int:id>", methods=["GET"])
def get_todo(id):
  todo = Todo.query.get_or_404(id)
  return jsonify(todo_to_dict(todo))

@app.route("/todos/<int:id>", methods=["PUT"])
def update_todo(id):
  todo = Todo.query.get_or_404(id)
  data = request.json
  todo.title = data.get("title", todo.title)
  todo.done = data.get("done", todo.done)
  db.session.commit()
  return jsonify(todo_to_dict(todo))

@app.route("todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
  todo = Todo.query.get_or_404(id)
  db.session.delete(todo)
  db.session.commit()
  return "", 404

@app.route("/")
def hello_world():
  """Example Hello World route."""
  name = os.environ.get("NAME", "World")
  return f"Hello {name}!"

if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))