"""
Módulo controller
-----------------
Conecta a View com o Model, controlando o fluxo de login.
Utiliza QThread para executar o login de forma assíncrona e manter a interface responsiva.
"""

from PySide6.QtCore import QThread, QTimer, Slot, QCoreApplication
from PySide6.QtWidgets import QApplication
from model import CanaimeLoginModel  # Todos os arquivos estão na raiz do projeto

# Importação do tipo Signal a partir do PySide6.QtCore
from PySide6.QtCore import Signal


class LoginThread(QThread):
    """
    Thread para executar o processo de login utilizando o Model.
    Emite sinais com o resultado do login para o Controller.

    Sinais:
        finished(bool, str, object): Emite (sucesso, nome_completo, page) ao terminar.
        error(str): Emite uma mensagem de erro, se ocorrer.
    """
    finished = Signal(bool, str, object)  # (success, full_name, page)
    error = Signal(str)

    def __init__(self, model: CanaimeLoginModel, username: str, password: str, parent=None):
        """
        Inicializa a thread com o model e as credenciais de login.

        Args:
            model (CanaimeLoginModel): Instância do Model para executar o login.
            username (str): Nome de usuário.
            password (str): Senha.
            parent: Objeto pai (opcional).
        """
        super().__init__(parent)
        self.model = model
        self.username = username
        self.password = password

    def run(self):
        """
        Executa o processo de login. Se o login for bem-sucedido,
        emite o sinal finished com (True, full_name, page). Se ocorrer algum erro,
        emite o sinal error com a mensagem de exceção.
        """
        try:
            success, full_name, page = self.model.perform_login(self.username, self.password)
            self.finished.emit(success, full_name, page)
        except Exception as e:
            self.error.emit(str(e))


class CanaimeLoginController:
    """
    Controller para gerenciar o fluxo de login.
    Conecta a interface (View) com a lógica de negócio (Model) e utiliza QThread para
    executar o processo de login de forma assíncrona.
    """

    def __init__(self, view, test_mode: bool = False) -> None:
        """
        Inicializa o Controller associando a View e instanciando o Model.

        Args:
            view: Instância da interface de login.
            test_mode (bool): Se True, o navegador roda em modo não-headless (visível).
        """
        self.view = view
        self.model = CanaimeLoginModel(test_mode=test_mode)
        self.login_thread = None  # Será atribuído a instância de LoginThread
        self._finalizing = False  # Flag para evitar finalizações múltiplas
        self._bind_events()

    def _bind_events(self) -> None:
        """
        Conecta os sinais dos widgets da View aos métodos do Controller.
        """
        # Conecta o clique no botão de login e o pressionar "Enter" no campo de senha
        self.view.login_btn.clicked.connect(self.start_login_process)
        self.view.password_input.returnPressed.connect(self.start_login_process)

    def start_login_process(self) -> None:
        """
        Inicia o fluxo de login:
          - Desabilita o botão de login e exibe uma mensagem de status.
          - Exibe o spinner de carregamento.
          - Cria e inicia a thread de login.
        """
        self.view.disable_login_button()
        self.view.set_status_message("Realizando login...")
        self.view.start_loading_animation()

        username = self.view.get_username()
        password = self.view.get_password()

        # Cria a thread de login
        self.login_thread = LoginThread(self.model, username, password)
        # Conecta os sinais da thread para tratar o resultado
        self.login_thread.finished.connect(self._on_login_finished)
        self.login_thread.error.connect(self._on_login_error)
        self.login_thread.start()

    @Slot(bool, str, object)
    def _on_login_finished(self, success: bool, full_name: str, page: object) -> None:
        """
        Trata o resultado do login.
        Se bem-sucedido, armazena o objeto page na View, exibe mensagem de boas-vindas
        e finaliza a aplicação. Caso contrário, exibe mensagem de erro e finaliza.
        """
        self.view.stop_loading_animation()
        if success:
            self.view.set_status_message(f"Bem vindo {full_name}!")
            self.view._login_result = page
        else:
            self.view.set_status_message("Usuário ou senha inválidos.")
            self.view._login_result = None

        # Aguarda 500ms para que o usuário veja a mensagem e, em seguida, finaliza
        QTimer.singleShot(500, self._finalize)

    @Slot(str)
    def _on_login_error(self, message: str) -> None:
        """
        Trata erros ocorridos durante o processo de login.
        Exibe a mensagem de erro e finaliza a aplicação.
        """
        self.view.stop_loading_animation()
        self.view.set_status_message(message)
        self.view._login_result = None
        QTimer.singleShot(500, self._finalize)

    def _finalize(self) -> None:
        """
        Encerra a thread (se ativa) e finaliza a aplicação.
        Essa função é executada apenas uma vez para evitar múltiplas finalizações.
        """
        if self._finalizing:
            return
        self._finalizing = True

        # Encerra a thread de login, se estiver ativa
        if self.login_thread is not None and self.login_thread.isRunning():
            self.login_thread.quit()
            self.login_thread.wait()
            self.login_thread = None

        # Fecha a janela e encerra o loop de eventos
        self.view.close()
        QApplication.instance().quit()
