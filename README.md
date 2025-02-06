
# Login Canaimé

**Login Canaimé** é uma biblioteca Python que fornece uma interface gráfica moderna para realizar o login no Sistema Canaimé, um sistema desenvolvido para gerenciar unidades prisionais e facilitar o controle de dados de reeducandos, dados administrativos, visitantes e acesso em tempo real a informações para órgãos como a Justiça, Defensoria Pública e Ministério Público.

A biblioteca integra o **Model**, **View** e **Controller** para fornecer um fluxo de login robusto e reutilizável. Além disso, ela utiliza o **PySide6** para a interface gráfica e o **Playwright** para automatizar o processo de login, permitindo a execução em modo headless (para produção) ou não-headless (para testes).

## Características

 1. **Interface moderna e personalizável:**
	  - Janela sem borda e fundo translúcido;
     - Campos de e-mail e senha (este último com caracteres ocultos);
     - Ícone personalizado (baixado a partir de uma URL);
     - Spinner de carregamento (GIF animado) durante o processo de login;
     - Janela arrastável (mesmo sem borda);

 2. **Fluxo de login assíncrono:**  
	 - Utiliza o QThread (via subclassificação de QThread) para executar o processo de login sem travar a interface;

 3. **Retorno do resultado:**  
	 - Retorna o objeto `Page` logado (do Playwright) para uso em aplicações reais;
	 - Permite também, em modo de desenvolvimento, obter as credenciais digitadas.

## Estrutura do Projeto

```markdown
📦 login-canaime_project/        # Diretório raiz do projeto
├── ⚙️ config.py                 # Configurações globais do projeto
├── 📋 requirements.txt          # Lista de dependências do projeto
├── 🛡️ LICENSE                   # Arquivo de licença do projeto
├── 📖 README.md                 # Documentação do projeto
└── 📦 loginCanaime/             # Pacote principal
    ├── 📄 __init__.py           # Inicializa o pacote e expõe a classe Login
    ├── 📄 model.py              # Lógica de negócio (Model, utilizando Playwright)
    ├── 📄 view.py               # Interface gráfica (View, utilizando PySide6)
    ├── 📄 controller.py         # Controle de fluxo (Controller, utilizando QThread)
    └── 📄 main.py               # Funções principais para login
   ```

 ## Instalação
O pacote pode ser instalado via pip. Depois de empacotar o projeto (o nome de distribuição é `login-canaime`), você pode instalá-lo com:

```bash
pip install login-canaime
``` 

> **Observação:**  
> O nome do pacote para importação é `loginCanaime`. Isso significa que, após a instalação, você usará:
> ```bash
> from loginCanaime import Login
> ```

## Uso

### Exemplo de Uso em Produção

Para iniciar o fluxo de login e obter o objeto `Page` logado (útil para integrar com outras aplicações que utilizam o Playwright):

```bash
from loginCanaime import Login

# Inicia o login; o parâmetro test_mode=False faz com que o navegador rode em modo headless
page = Login.run(test_mode=False)
if page:
    print("Login efetuado com sucesso!")
    # Utilize o objeto page conforme necessário...
else:
    print("Falha no login ou o login foi cancelado.")
   ```

### Exemplo de Uso em Desenvolvimento
Se você quiser apenas obter as credenciais digitadas (por exemplo, para testes):

```bash
from loginCanaime import Login

credentials = Login.get_credentials(test_mode=False)
print("Credenciais digitadas:", credentials)
``` 

## Funcionamento Interno

-   **Model:**  
    O módulo `model.py` utiliza o Playwright para abrir o navegador, navegar até a página de login e preencher os campos de usuário e senha.  
    Ele utiliza uma heurística baseada no conteúdo de um elemento específico da página para confirmar o sucesso do login e retorna uma tupla `(True, full_name, page)` ou `(False, "", None)`.
    
-   **View:**  
    O módulo `view.py` implementa a interface gráfica com PySide6, contendo campos para e-mail e senha, botão de login, label de status e um spinner de carregamento (GIF).  
    A interface é configurada sem borda, com um ícone personalizado (baixado de uma URL) e permite arrastar a janela.
    
-   **Controller:**  
    O módulo `controller.py` conecta a View e o Model. Utiliza um QThread (via subclassificação de QThread na classe `LoginThread`) para executar o login de forma assíncrona, mantendo a interface responsiva.  
    O Controller finaliza o aplicativo automaticamente assim que o login é concluído, retornando o objeto `Page` logado.
    

## Contribuição

Contribuições são bem-vindas! Se você deseja melhorar o código, adicione novas funcionalidades ou corrigir problemas, sinta-se à vontade para abrir _issues_ ou enviar _pull requests_.



## Contato

Anderson Assunção – andersongomesrr@hotmail.com  
Projeto disponível em: [https://github.com/A-Assuncao/login-canaime_project](https://github.com/A-Assuncao/login-canaime_project)

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENÇA](LICENSE) para mais detalhes.  
  
----------  
**Desenvolvido com ♥ e Python.**