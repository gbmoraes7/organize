from models import db


class Investimento(db.Model):
    __tablename__ = "investimentos"

    id = db.Column(db.Integer, primary_key=True)

    descricao = db.Column(db.String(200), nullable=False)

    meta = db.Column(db.Float, nullable=False)

    valor_investido = db.Column(db.Float, nullable=False)
