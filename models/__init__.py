"""Camada Model.

A instância ``db`` é criada aqui, uma única vez, e é a mesma usada por todos
os modelos. Ela precisa existir ANTES de importar os módulos abaixo, porque
eles fazem ``from models import db``.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.lancamento import Lancamento  
from models.investimento import Investimento 
from models.aporte import Aporte 

__all__ = ["db", "Lancamento", "Investimento", "Aporte"]

