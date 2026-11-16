import os

from dotenv import load_dotenv

load_dotenv()

from flask import Flask

from controllers import home, investimentos, lancamentos, relatorios
from models import db

app = Flask(__name__, template_folder="views")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(home.bp)
app.register_blueprint(lancamentos.bp)
app.register_blueprint(investimentos.bp)
app.register_blueprint(relatorios.bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
