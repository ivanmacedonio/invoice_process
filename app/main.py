from flask import Flask
from flask_cors import CORS
from routes import register_blueprints

app = Flask(__name__)
CORS(app, origins='*')

if __name__ == "__main__":
    register_blueprints(app)
    app.run(debug=True, host='0.0.0.0', port=3000)
