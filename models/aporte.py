from datetime import date

from models import db


class Aporte(db.Model):
    __tablename__ = "aportes"

    id = db.Column(db.Integer, primary_key=True)
    investimento_id = db.Column(
        db.Integer,
        db.ForeignKey("investimentos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False, default=date.today)