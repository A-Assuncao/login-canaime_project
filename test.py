#!/usr/bin/env python
"""
Exemplo de uso da biblioteca login-canaime.

Este script demonstra as duas maneiras principais de usar a biblioteca:
1. Obter apenas as credenciais
2. Obter a página logada para manipulação
"""

from login_canaime import Login
import time


def exemplo_credenciais():
    """Demonstra como obter apenas as credenciais."""
    print("\n=== EXEMPLO 1: OBTER APENAS CREDENCIAIS ===")
    
    login = Login()
    usuario, senha = login.obter_credenciais()
    
    if usuario and senha:
        print(f"Login bem-sucedido!")
        print(f"Usuário: {usuario}")
        print(f"Senha: {'*' * len(senha)}")  # Oculta a senha por segurança
        
        # Aqui você pode usar as credenciais em outra aplicação
        print("\nAgora você pode usar essas credenciais em outro sistema.")
    else:
        print("Não foi possível obter as credenciais.")


def exemplo_pagina():
    """Demonstra como obter e manipular a página logada."""
    print("\n=== EXEMPLO 2: OBTER E MANIPULAR PÁGINA LOGADA ===")
    
    login = Login()
    page = login.obter_pagina(headless=False)
    
    if page:
        try:
            print(f"Login realizado com sucesso como: {login.usuario}")
            
            # Aqui começa a manipulação da página
            print("\n=== Manipulando a página ===")
            print(f"Título: {page.title()}")
            
            # Extrair dados da página
            if page.locator("table").count() > 0:
                print("\n=== Dados de Tabelas ===")
                tabelas = page.locator("table").all()
                for i, tabela in enumerate(tabelas):
                    print(f"Tabela {i+1}: {tabela.locator('tr').count()} linhas")
            
            # Interagir com a navegação
            if page.locator("nav a").count() > 0:
                print("\n=== Links de Navegação ===")
                menus = page.locator("nav a").all()
                print(f"Menus disponíveis: {len(menus)}")
            
            # Navegar para outra página (Google como exemplo)
            print("\n=== Navegando para o Google ===")
            try:
                # Capturar screenshot antes
                page.screenshot(path="antes_navegacao.png")
                print("Screenshot 'antes_navegacao.png' salvo")
                
                # Navegar para o Google
                page.goto("https://www.google.com", wait_until="networkidle")
                print(f"Navegação concluída. Novo título: {page.title()}")
                
                # Capturar screenshot depois
                page.screenshot(path="apos_navegacao.png")
                print("Screenshot 'apos_navegacao.png' salvo")
            except Exception as e:
                print(f"Erro ao navegar: {str(e)}")
            
            # Aguardar para visualização
            print("\nAguardando 10 segundos para visualização...")
            time.sleep(10)
            
        finally:
            # Sempre feche o navegador quando terminar
            print("Fechando o navegador...")
            login.fechar()
            print("Navegador fechado.")
    else:
        print("Não foi possível obter a página logada.")


def main():
    """Função principal que executa os exemplos."""
    print("=== DEMONSTRAÇÃO DA BIBLIOTECA LOGIN-CANAIME ===")
    
    # Perguntar qual exemplo executar
    print("\nQual exemplo deseja executar?")
    print("1. Obter apenas credenciais")
    print("2. Obter e manipular página logada")
    print("3. Executar ambos os exemplos")
    
    try:
        escolha = int(input("Digite o número (1, 2 ou 3): "))
        
        if escolha == 1:
            exemplo_credenciais()
        elif escolha == 2:
            exemplo_pagina()
        elif escolha == 3:
            exemplo_credenciais()
            exemplo_pagina()
        else:
            print("Opção inválida!")
    except ValueError:
        print("Por favor, digite um número válido.")
    
    print("\n=== FIM DA DEMONSTRAÇÃO ===")


if __name__ == "__main__":
    main() 