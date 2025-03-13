from login_canaime import Login


with Login() as login:
    page = login.obter_pagina()    
    if page:
        print(f"Título da página: {page.title()}")
        
        # Fazer operações...
        
        page.goto("https://www.google.com")        
        page.screenshot(path="screenshot.png")
        page.wait_for_timeout(10000)
        
# O navegador será fechado automaticamente ao sair do bloco 'with'