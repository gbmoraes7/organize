"""Camada Model.

A instância ``db`` é criada aqui, uma única vez, e é a mesma usada por todos
os modelos. Ela precisa existir ANTES de importar os módulos abaixo, porque
eles fazem ``from models import db``.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.lancamento import Lancamento  # noqa: E402
from models.investimento import Investimento  # noqa: E402

__all__ = ["db", "Lancamento", "Investimento"]
