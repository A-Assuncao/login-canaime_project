# login-canaime

<p align="center">
  <img src="https://github.com/A-Assuncao/login-canaime_project/blob/main/login_canaime/images/brasao.png" alt="Login Canaime Logo" width="200"/>
</p>

**login-canaime** é uma biblioteca Python que simplifica a autenticação e manipulação do sistema Canaimé. Utilizando o Playwright para automação de navegação web, esta biblioteca permite autenticar-se no sistema Canaimé e obter uma página já logada para manipulação direta.

## Sumário

- [Principais Recursos](#principais-recursos)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Uso como Biblioteca](#uso-como-biblioteca)
  - [Obter apenas as credenciais](#1-obter-apenas-as-credenciais)
  - [Obter e manipular a página logada](#2-obter-e-manipular-a-página-logada)
  - [Uso com gerenciador de contexto](#3-uso-com-gerenciador-de-contexto)
- [Autenticadores Alternativos](#autenticadores-alternativos)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Principais Recursos

- 🔑 **Autenticação Simplificada**: Interface gráfica para inserção de credenciais
- 🌐 **Acesso Direto à Página**: Retorna a página já logada para manipulação direta com Playwright
- 🛠️ **API Flexível**: Múltiplas formas de autenticação (GUI, argumentos, variáveis de ambiente)
- 📦 **Fácil Integração**: Construída como uma biblioteca Python padrão, fácil de integrar em seus projetos
- 🔄 **Compatibilidade**: Funciona com Python 3.8+ em Windows, macOS e Linux

## Requisitos

- [Python 3.8+](https://www.python.org/) (recomendado Python 3.9 ou superior)
- [Playwright](https://pypi.org/project/playwright/) (≥ 1.28.0)

## Instalação

```bash
# Instalação via pip
pip install login-canaime

# Instalação dos navegadores do Playwright (necessário apenas na primeira vez)
playwright install
```

## Uso como Biblioteca

A biblioteca `login-canaime` oferece várias maneiras de autenticar-se no sistema Canaimé:

### 1. Obter apenas as credenciais

```python
from login_canaime import Login

# Criar uma instância da classe Login
login = Login()

# Obter apenas as credenciais
usuario, senha = login.obter_credenciais()

if usuario and senha:
    print(f"Login bem-sucedido! Usuário: {usuario}")
    
    # Usar as credenciais em outro sistema
    # outro_sistema.login(usuario, senha)
```

### 2. Obter e manipular a página logada

```python
from login_canaime import Login
import time

# Criar uma instância da classe Login
login = Login()

# Obter a página logada
page = login.obter_pagina(headless=False)

if page:
    try:
        print(f"Login realizado como: {login.usuario}")
        
        # Manipular a página com Playwright
        print(f"Título da página: {page.title()}")
        
        # Capturar screenshot
        page.screenshot(path="screenshot.png")
        
        # Navegar para outra página
        page.goto("https://www.google.com")
        
        # Aguardar visualização
        time.sleep(5)
        
    finally:
        # Sempre feche o navegador ao terminar
        login.fechar()
```

### 3. Uso com gerenciador de contexto

```python
from login_canaime import Login
import time

# Usando com o gerenciador de contexto 'with'
with Login() as login:
    # Obter a página logada
    page = login.obter_pagina()
    
    if page:
        print(f"Título da página: {page.title()}")
        
        # Fazer operações...
        
        # Aguardar visualização
        time.sleep(5)
    
# O navegador será fechado automaticamente ao sair do bloco 'with'
```

## Autenticadores Alternativos

A biblioteca suporta diferentes métodos de autenticação:

```python
from login_canaime import Login, AutenticadorArgs, AutenticadorEnv

# 1. Usando credenciais em argumentos
auth_args = AutenticadorArgs()
login1 = Login(autenticador=auth_args)
page = login1.obter_pagina(usuario="usuario_exemplo", senha="senha_exemplo")

# 2. Usando variáveis de ambiente (CANAIME_USUARIO e CANAIME_SENHA)
auth_env = AutenticadorEnv()
login2 = Login(autenticador=auth_env)
page = login2.obter_pagina()
```

## Estrutura do Projeto

```
📦 login-canaime/
├── 📂 login_canaime/        # Pacote principal
│   ├── 📄 __init__.py       # Exporta as classes principais
│   ├── 📄 auth.py           # Classe Login principal 
│   ├── 📄 autenticador.py   # Classes para autenticação
│   ├── 📄 cli.py            # Interface de linha de comando
│   └── 📂 ui/               # Interfaces gráficas
│       └── 📄 tkinter_ui.py # Componentes de UI (migrar para PySide6)
├── 📄 pyproject.toml        # Configuração do projeto
├── 📄 setup.py              # Script de instalação
├── 📄 LICENSE               # Licença MIT
└── 📄 README.md             # Esta documentação
```

## Contribuição

Contribuições são sempre bem-vindas! Sinta-se à vontade para:

1. Abrir _Issues_ relatando bugs ou sugerindo melhorias.
2. Criar _Pull Requests_ com correções ou novas funcionalidades.
3. Entrar em contato para discutir novas ideias antes de implementar.

Para contribuir:

```bash
# Clone o repositório
git clone https://github.com/A-Assuncao/login-canaime.git
cd login-canaime

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac

# ou
venv\Scripts\activate     # Windows

# Instale em modo de desenvolvimento
pip install -e .
```

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSA](LICENSE.md) para mais detalhes.

---

**Desenvolvido com ♥ por [Anderson Assunção](https://github.com/A-Assuncao)** 