
from dataclasses import dataclass, field
from typing import List

from calculos import TIPO_DESPESA_EMERGENCIAL, TIPO_RECEITA, calcular_saldo


@dataclass
class GastoCategoria:
    nome: str
    valor: float
    porcentagem: float


@dataclass
class RelatorioFinanceiro:
    total_receitas: float = 0
    total_despesas: float = 0
    total_investido: float = 0
    saldo_final: float = 0
    total_emergencial: float = 0
    porcentagem_emergencial: float = 0
    categorias: List[GastoCategoria] = field(default_factory=list)


class ServicoRelatorio:
    def gerar(self, lancamentos, investimentos, *, total_investido=None):
        
        lancamentos = list(lancamentos)

        if total_investido is None:
            total_investido = sum(i.valor_investido for i in investimentos)

        total_receitas = sum(
            l.valor for l in lancamentos if l.tipo == TIPO_RECEITA
        )
        total_despesas = sum(
            l.valor for l in lancamentos if l.tipo != TIPO_RECEITA
        )
        total_emergencial = sum(
            l.valor for l in lancamentos if l.tipo == TIPO_DESPESA_EMERGENCIAL
        )

        saldo_final = calcular_saldo(total_receitas, total_despesas, total_investido)

        return RelatorioFinanceiro(
            total_receitas=total_receitas,
            total_despesas=total_despesas,
            total_investido=total_investido,
            saldo_final=saldo_final,
            total_emergencial=total_emergencial,
            porcentagem_emergencial=self._porcentagem(total_emergencial, total_despesas),
            categorias=self._gastos_por_categoria(lancamentos, total_despesas),
        )

    @staticmethod
    def _porcentagem(parte, total):
        if total > 0:
            return (parte / total) * 100
        return 0

    def _gastos_por_categoria(self, lancamentos, total_despesas):
        totais = {}
        for l in lancamentos:
            if l.tipo != TIPO_RECEITA:
                totais[l.categoria] = totais.get(l.categoria, 0) + l.valor

        return [
            GastoCategoria(
                nome=nome,
                valor=valor,
                porcentagem=self._porcentagem(valor, total_despesas),
            )
            for nome, valor in totais.items()
        ]
