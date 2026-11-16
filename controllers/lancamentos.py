from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for

from models import Lancamento, db

bp = Blueprint("lancamentos", __name__)


@bp.route("/lancamentos")
def listar():
    categoria = request.args.get("categoria")

    if categoria and categoria != "Todas as categorias":
        lista_lancamentos = Lancamento.query.filter_by(
            categoria=categoria
        ).all()
    else:
        lista_lancamentos = Lancamento.query.all()

    return render_template(
        "lancamentos.html",
        lancamentos=lista_lancamentos
    )


@bp.route("/adicionar-lancamento", methods=["POST"])
def adicionar():
    tipo = request.form["tipo"]
    descricao = request.form["descricao"]
    valor = float(request.form["valor"])
    categoria = request.form["categoria"]

    data = datetime.strptime(
        request.form["data"],
        "%Y-%m-%d"
    )

    novo_lancamento = Lancamento(
        tipo=tipo,
        descricao=descricao,
        valor=valor,
        categoria=categoria,
        data=data
    )

    db.session.add(novo_lancamento)
    db.session.commit()

    origem = request.form.get("origem")

    if origem == "home":
        return redirect(url_for("home.index"))

    return redirect(url_for("lancamentos.listar"))


@bp.route("/editar-lancamento/<int:id>")
def editar(id):
    lancamento = Lancamento.query.get_or_404(id)

    return render_template(
        "editar_lancamento.html",
        lancamento=lancamento
    )


@bp.route("/atualizar-lancamento/<int:id>", methods=["POST"])
def atualizar(id):
    lancamento = Lancamento.query.get_or_404(id)

    lancamento.tipo = request.form["tipo"]
    lancamento.descricao = request.form["descricao"]
    lancamento.valor = float(request.form["valor"])
    lancamento.categoria = request.form["categoria"]
    lancamento.data = request.form["data"]

    db.session.commit()

    return redirect(url_for("lancamentos.listar"))


@bp.route("/excluir-lancamento/<int:id>")
def excluir(id):
    lancamento = Lancamento.query.get_or_404(id)

    db.session.delete(lancamento)
    db.session.commit()

    return redirect(url_for("lancamentos.listar"))
