"""
Módulo model
------------
Contém a lógica de negócio (regras e acessos externos) para login no Canaimé.
Utiliza o Playwright para automatizar o fluxo de login.
"""

from typing import Tuple, Optional
from playwright.sync_api import sync_playwright, Browser, Page

# URL de login do sistema Canaimé
LOGIN_URL: str = "https://canaime.com.br/sgp2rr/login/login_principal.php"


class CanaimeLoginModel:
    """
    Classe responsável por encapsular a lógica de login utilizando Playwright.

    Essa classe executa os fluxos de login. Em vez de utilizar uma heurística baseada
    na contagem de imagens, agora captura o conteúdo do elemento contendo o nome do usuário
    e o login, comparando o login capturado com o valor informado. Se coincidir, considera o login bem-sucedido,
    imprimindo "Bem vindo {nome_completo_usuario}".
    """

    def __init__(self, test_mode: bool = False) -> None:
        """
        Inicializa a classe de modelo.

        Args:
            test_mode (bool): Se True, o navegador é aberto em modo não-headless (visível).
                              Caso contrário, roda em modo headless.
        """
        self.test_mode: bool = test_mode
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    def perform_login(self, username: str, password: str) -> Tuple[bool, str, Optional[Page]]:
        if not username or not password:
            raise ValueError("Usuário e senha são obrigatórios.")

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=not self.test_mode)
        context = self.browser.new_context()
        self.page = context.new_page()

        self.page.goto(LOGIN_URL)
        self.page.fill("input[name='usuario']", username)
        self.page.fill("input[name='senha']", password)
        self.page.press("input[name='senha']", "Enter")
        self.page.wait_for_timeout(5000)

        frame = self.page.frame(name="areas")
        if not frame:
            return False, "", None

        locator = frame.locator(".tituloAmarelo")
        text = locator.text_content()
        if not text:
            return False, "", None

        text = text.strip()
        parts = text.splitlines()
        if len(parts) < 2:
            return False, "", None

        full_name = parts[0].strip()
        login_obtained = parts[1].strip()

        if login_obtained == username:
            print(f"Bem vindo {full_name}")
            return True, full_name, self.page
        else:
            return False, "", None

    def login_js_images_disabled(self, username: str, password: str) -> Page:
        """
        Realiza o processo de login com o JavaScript desabilitado e bloqueio de imagens.
        """
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=not self.test_mode)
            context = browser.new_context(
                java_script_enabled=False,
                extra_http_headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                }
            )
            context.route("**/*", lambda route: (
                route.abort() if route.request.resource_type == "image" else route.continue_()
            ))
            page: Page = context.new_page()
            page.goto(LOGIN_URL)
            page.fill("input[name='usuario']", username)
            page.fill("input[name='senha']", password)
            page.press("input[name='senha']", "Enter")
            return page
