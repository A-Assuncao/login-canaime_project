import sys
from typing import Optional, Tuple
from PySide6.QtWidgets import QApplication
from view import CanaimeLoginView
from controller import CanaimeLoginController
from playwright.sync_api import Page  # Para anotação de tipos


class Login:
    """
    Classe principal para realizar o login no Sistema Canaimé.

    Métodos:
        run(test_mode: bool = False) -> Optional[Page]:
            Inicia o fluxo de login e retorna o objeto Page logado se o login for bem-sucedido.

        get_credentials(test_mode: bool = False) -> Tuple[str, str]:
            Inicia o fluxo de login e retorna uma tupla (login, senha) digitada pelo usuário.
    """

    @staticmethod
    def run(test_mode: bool = False) -> Optional[Page]:
        """
        Exibe a interface de login e retorna a página logada (Page) se o login for bem-sucedido.
        Essa função é a principal para aplicações que desejam reutilizar a biblioteca.

        Args:
            test_mode (bool): Define se o navegador roda em modo visível.

        Returns:
            Optional[Page]: Objeto Page logado ou None se o login falhar.
        """
        app = QApplication(sys.argv)
        view = CanaimeLoginView()
        # Inicializa a propriedade de resultado para armazenar o objeto Page logado
        view._login_result = None
        # Instancia o Controller, que irá gerenciar o fluxo de login
        _ = CanaimeLoginController(view, test_mode=test_mode)
        view.show()
        app.exec()
        return view._login_result

    @staticmethod
    def get_credentials(test_mode: bool = False) -> Tuple[str, str]:
        """
        Exibe a interface de login e retorna uma tupla (login, senha) digitada pelo usuário.
        Essa função é destinada a desenvolvimento.

        Args:
            test_mode (bool): Define se o navegador roda em modo visível.

        Returns:
            Tuple[str, str]: Tuple contendo (login, senha).
        """
        app = QApplication(sys.argv)
        view = CanaimeLoginView()
        _ = CanaimeLoginController(view, test_mode=test_mode)
        view.show()
        app.exec()
        return (view.get_username(), view.get_password())


if __name__ == "__main__":
    # Exemplo de uso:
    # Para realizar o login e obter a página logada:
    page = Login.run(test_mode=False)
    if page:
        print("Login efetuado com sucesso!")
    else:
        print("Login falhou ou foi cancelado.")
