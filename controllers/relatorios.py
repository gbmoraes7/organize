from datetime import date

from flask import Blueprint, render_template, request
from sqlalchemy import func

from models import Aporte, Investimento, Lancamento, db
from services.servico_relatorio import ServicoRelatorio

bp = Blueprint("relatorios", __name__)

servico_relatorio = ServicoRelatorio()

# Raio do SVG e quantidade de cores de serie no CSS.
CIRCUNFERENCIA = 2 * 3.1416 * 66
QUANTIDADE_SERIES = 7

@bp.route("/relatorios")
def exibir():
    inicio_lancamentos, fim_lancamentos = db.session.query(
        func.min(Lancamento.data), func.max(Lancamento.data)
    ).one()

    inicio_aportes, fim_aportes = db.session.query(
        func.min(Aporte.data), func.max(Aporte.data)
    ).one()

    inicios = [d for d in (inicio_lancamentos, inicio_aportes) if d is not None]
    fins = [d for d in (fim_lancamentos, fim_aportes) if d is not None]

    data_minima = min(inicios, default=None)
    data_maxima = max(fins, default=None)

    minimo = data_minima.isoformat() if data_minima is not None else ""
    maximo = data_maxima.isoformat() if data_maxima is not None else ""

    filtrado = "data_inicial" in request.args or "data_final" in request.args
    contexto = {
        "data_minima": minimo,
        "data_maxima": maximo,
        "data_inicial": request.args.get("data_inicial", "") if filtrado else minimo,
        "data_final": request.args.get("data_final", "") if filtrado else maximo,
    }

    query = Lancamento.query

    if filtrado:
        try:
            inicio, fim = _validar_periodo(
                contexto["data_inicial"],
                contexto["data_final"],
                data_minima,
                data_maxima,
            )
        except ValueError as erro:
            return render_template(
                "relatorios.html", erro=str(erro), **contexto
            ), 400

        query = query.filter(
            Lancamento.data >= inicio,
            Lancamento.data <= fim,
        )

        total_aportado = db.session.query(
            func.coalesce(func.sum(Aporte.valor), 0.0)
        ).filter(
            Aporte.data >= inicio,
            Aporte.data <= fim,
        ).scalar()

        relatorio = servico_relatorio.gerar(
            query.all(), [], total_investido=total_aportado
        )
    else:
        relatorio = servico_relatorio.gerar(
            query.all(), Investimento.query.all()
        )

    return render_template(
        "relatorios.html",
        **contexto,
        filtrado=filtrado,
        total_receitas=relatorio.total_receitas,
        total_despesas=relatorio.total_despesas,
        total_investido=relatorio.total_investido,
        saldo_final=relatorio.saldo_final,
        total_emergencial=relatorio.total_emergencial,
        porcentagem_emergencial=relatorio.porcentagem_emergencial,
        categorias=_montar_segmentos_donut(relatorio.categorias),
    )

def _validar_periodo(inicio_texto, fim_texto, data_minima, data_maxima):
    if data_minima is None or data_maxima is None:
        raise ValueError("Ainda não há lançamentos ou aportes para filtrar.")

    if not inicio_texto or not fim_texto:
        raise ValueError("Preencha a data inicial e a data final.")

    try:
        inicio = date.fromisoformat(inicio_texto)
        fim = date.fromisoformat(fim_texto)
    except ValueError:
        raise ValueError("Informe datas válidas.") from None

    if inicio.isoformat() != inicio_texto or fim.isoformat() != fim_texto:
        raise ValueError("Informe datas válidas.")

    if inicio > fim:
        raise ValueError("A data inicial não pode ser posterior à data final.")

    if inicio < data_minima or fim > data_maxima:
        raise ValueError("Escolha datas dentro do intervalo disponível.")

    return inicio, fim


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
