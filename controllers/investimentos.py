from flask import Blueprint, redirect, render_template, request, url_for
from math import isfinite
from datetime import date
from calculos import resumir_investimentos
from models import Aporte, Investimento, db

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

    if novo_investimento.valor_investido > 0:
        db.session.flush()  # Obtém o ID da meta sem confirmar a transação.
        db.session.add(Aporte(
            investimento_id=novo_investimento.id,
            valor=novo_investimento.valor_investido,
        ))

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


@bp.route("/investimentos/<int:id>/aportes/novo", methods=["GET", "POST"])
def adicionar_aporte(id):
    consulta = Investimento.query.filter_by(id=id)

    if request.method == "POST":
        consulta = consulta.with_for_update()

    investimento = consulta.first_or_404()

    if request.method == "GET":
        return render_template(
            "adicionar_aporte.html",
            investimento=investimento,
            data_selecionada=date.today().isoformat(),
        )

    data_digitada = request.form.get("data_aporte", "")

    try:
        valor = float(request.form.get("valor", ""))
    except ValueError:
        valor = 0

    if not isfinite(valor) or valor < 0.01:
        return render_template(
            "adicionar_aporte.html",
            investimento=investimento,
            data_selecionada=data_digitada,
            erro="Informe um valor de pelo menos R$ 0,01.",
        ), 400

    try:
        data_aporte = date.fromisoformat(data_digitada)
    except ValueError:
        return render_template(
            "adicionar_aporte.html",
            investimento=investimento,
            data_selecionada=data_digitada,
            erro="Informe uma data válida para o aporte.",
        ), 400

    investimento.valor_investido += valor
    db.session.add(
        Aporte(
            investimento_id=investimento.id,
            valor=valor,
            data=data_aporte,
        )
    )
    db.session.commit()

    return redirect(url_for("investimentos.listar"))
    
    
