from flask import Blueprint, redirect, render_template, request, url_for

from calculos import resumir_investimentos
from models import Investimento, db

bp = Blueprint("investimentos", __name__)


@bp.route("/investimentos")
def listar():
    investimentos = Investimento.query.all()

    resumo = resumir_investimentos(investimentos)

    return render_template(
        "investimentos.html",
        investimentos=investimentos,
        **resumo
    )


@bp.route("/adicionar-investimento", methods=["POST"])
def adicionar():
    novo_investimento = Investimento(
        descricao=request.form.get("descricao"),
        meta=float(request.form.get("meta")),
        valor_investido=float(request.form.get("valor_investido"))
    )

    db.session.add(novo_investimento)
    db.session.commit()

    return redirect(url_for("investimentos.listar"))


@bp.route("/excluir-investimento/<int:id>")
def excluir(id):
    investimento = Investimento.query.get_or_404(id)

    db.session.delete(investimento)
    db.session.commit()

    return redirect(url_for("investimentos.listar"))


@bp.route("/editar-investimento/<int:id>", methods=["GET", "POST"])
def editar(id):
    investimento = Investimento.query.get_or_404(id)

    if request.method == "POST":
        _copiar_formulario(investimento)
        db.session.commit()

        return redirect(url_for("investimentos.listar"))

    return render_template(
        "editar_investimento.html",
        investimento=investimento
    )


@bp.route("/atualizar-investimento/<int:id>", methods=["POST"])
def atualizar(id):
    investimento = Investimento.query.get_or_404(id)

    _copiar_formulario(investimento)
    db.session.commit()

    return redirect(url_for("investimentos.listar"))


def _copiar_formulario(investimento):
    investimento.descricao = request.form.get("descricao")
    investimento.meta = float(request.form.get("meta"))
    investimento.valor_investido = float(request.form.get("valor_investido"))
