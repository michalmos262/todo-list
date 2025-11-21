from flask import Flask
from controller.todos_controller import TodosController

app = Flask(__name__)
HOST = "0.0.0.0"
PORT = 8574

if __name__ == "__main__":
    todos_controller = TodosController(app)
    app.run(host=HOST, port=PORT)