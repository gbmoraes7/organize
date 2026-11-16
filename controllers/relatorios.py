from flask import Blueprint, render_template, request
from sqlalchemy import extract

from models import Investimento, Lancamento
from services.servico_relatorio import ServicoRelatorio

bp = Blueprint("relatorios", __name__)

servico_relatorio = ServicoRelatorio()


CIRCUNFERENCIA = 2 * 3.1416 * 66
QUANTIDADE_SERIES = 7

@bp.route("/relatorios")
def exibir():
    lancamentos = _consultar_lancamentos_filtrados()

    investimentos = Investimento.query.all()

    relatorio = servico_relatorio.gerar(lancamentos, investimentos)

    return render_template(
        "relatorios.html",

        total_receitas=relatorio.total_receitas,
        total_despesas=relatorio.total_despesas,
        total_investido=relatorio.total_investido,
        saldo_final=relatorio.saldo_final,

        total_emergencial=relatorio.total_emergencial,
        porcentagem_emergencial=relatorio.porcentagem_emergencial,

        categorias=_montar_segmentos_donut(relatorio.categorias)
    )


def _consultar_lancamentos_filtrados():
    data_inicial = request.args.get("data_inicial")
    data_final = request.args.get("data_final")
    mes = request.args.get("mes")
    ano = request.args.get("ano")

    query = Lancamento.query

    if data_inicial:
        query = query.filter(Lancamento.data >= data_inicial)

    if data_final:
        query = query.filter(Lancamento.data <= data_final)

    if mes and mes != "Todos":
        query = query.filter(
            extract("month", Lancamento.data) == int(mes)
        )

    if ano:
        query = query.filter(
            extract("year", Lancamento.data) == int(ano)
        )

    return query.all()


def _montar_segmentos_donut(categorias):
    segmentos = []
    deslocamento = 0

    for i, categoria in enumerate(categorias):
        tamanho = (categoria.porcentagem / 100) * CIRCUNFERENCIA
        restante = CIRCUNFERENCIA - tamanho

        segmentos.append({
            "nome": categoria.nome,
            "valor": categoria.valor,
            "porcentagem": categoria.porcentagem,
            "serie": i % QUANTIDADE_SERIES + 1,
            "dasharray": f"{tamanho} {restante}",
            "dashoffset": -deslocamento
        })

        deslocamento += tamanho

    return segmentos
