
TIPO_RECEITA = "Receita"
TIPO_DESPESA_EMERGENCIAL = "Despesa Emergencial"


def calcular_saldo(receitas, despesas, investimentos):
    return receitas - despesas - investimentos


def somar_lancamentos(lancamentos):
    
    total_receitas = 0
    total_despesas = 0
    total_emergencial = 0
    total_nao_emergencial = 0

    for lancamento in lancamentos:
        if lancamento.tipo == TIPO_RECEITA:
            total_receitas += lancamento.valor
        elif lancamento.tipo == TIPO_DESPESA_EMERGENCIAL:
            total_despesas += lancamento.valor
            total_emergencial += lancamento.valor
        else:
            total_despesas += lancamento.valor
            total_nao_emergencial += lancamento.valor

    return total_receitas, total_despesas, total_emergencial, total_nao_emergencial


def somar_investido(investimentos):
    return sum(investimento.valor_investido for investimento in investimentos)


def calcular_porcentagens_saldo(total_receitas, total_despesas, total_investido):

    saldo = calcular_saldo(total_receitas, total_despesas, total_investido)
    total_saida = total_despesas + total_investido
    total_movimentado = total_receitas + total_saida

    if total_movimentado > 0:
        porcentagem_gasto = (total_saida / total_movimentado) * 100
        porcentagem_nao_gasto = (saldo / total_receitas) * 100 if total_receitas > 0 else 0
    else:
        porcentagem_gasto = 0
        porcentagem_nao_gasto = 0

    if porcentagem_nao_gasto < 0:
        porcentagem_nao_gasto = 0

    return porcentagem_gasto, porcentagem_nao_gasto


def calcular_porcentagens_emergencial(total_emergencial, total_nao_emergencial):

    total_despesas = total_emergencial + total_nao_emergencial

    if total_despesas > 0:
        return (
            (total_emergencial / total_despesas) * 100,
            (total_nao_emergencial / total_despesas) * 100,
        )
    return 0, 0


def calcular_resumo_home(lancamentos, investimentos):
    
    (total_receitas, total_despesas,
     total_emergencial, total_nao_emergencial) = somar_lancamentos(lancamentos)
    total_investido = somar_investido(investimentos)

    porcentagem_gasto, porcentagem_nao_gasto = calcular_porcentagens_saldo(
        total_receitas, total_despesas, total_investido
    )
    porcentagem_emergencial, porcentagem_nao_emergencial = (
        calcular_porcentagens_emergencial(total_emergencial, total_nao_emergencial)
    )

    return {
        "saldo": calcular_saldo(total_receitas, total_despesas, total_investido),
        "porcentagem_gasto": porcentagem_gasto,
        "porcentagem_nao_gasto": porcentagem_nao_gasto,
        "porcentagem_emergencial": porcentagem_emergencial,
        "porcentagem_nao_emergencial": porcentagem_nao_emergencial,
    }


def resumir_investimentos(investimentos):
    return {
        "total_investido": somar_investido(investimentos),
        "total_metas": sum(i.meta for i in investimentos),
        "metas_concluidas": len([
            i for i in investimentos if i.valor_investido >= i.meta
        ]),
        "metas_andamento": len([
            i for i in investimentos if i.valor_investido < i.meta
        ]),
    }
