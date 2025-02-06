"""
Pacote login_canaime
--------------------
Este pacote fornece as classes e funções necessárias para gerenciar o login no sistema Canaimé,
incluindo o Model, a View e o Controller.
"""

__version__ = "1.0.0"

from .model import CanaimeLoginModel
from .view import CanaimeLoginView
from .controller import CanaimeLoginController
from .main import Login
