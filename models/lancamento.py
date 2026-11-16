from models import db


class Lancamento(db.Model):
    __tablename__ = "lancamentos"

    id = db.Column(db.Integer, primary_key=True)

    tipo = db.Column(db.String(20), nullable=False)

    descricao = db.Column(db.String(200), nullable=False)

    valor = db.Column(db.Float, nullable=False)

    categoria = db.Column(db.String(50), nullable=False)

    data = db.Column(db.Date, nullable=False)
