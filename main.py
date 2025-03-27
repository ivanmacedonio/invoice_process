from flask import Flask
from flask_cors import CORS
from app.routes import register_blueprints
from app.services.bill_print import BillPrint

app = Flask(__name__)
CORS(app, origins='*')

if __name__ == "__main__":
    register_blueprints(app)
    BillPrint().write_pdf(payload={})
    # app.run(debug=True, host='0.0.0.0', port=3001)
