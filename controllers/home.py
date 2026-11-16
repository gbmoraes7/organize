from flask import Blueprint, render_template

from calculos import calcular_resumo_home
from models import Investimento, Lancamento

bp = Blueprint("home", __name__)


@bp.route("/")
def index():
    lancamentos = Lancamento.query.all()
    investimentos = Investimento.query.all()

    resumo = calcular_resumo_home(lancamentos, investimentos)

    return render_template("index.html", **resumo)
