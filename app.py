from flask import Flask
from flask_cors import CORS
from routes.search import search_blueprint
app = Flask(__name__)
app.register_blueprint(search_blueprint)
CORS(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)