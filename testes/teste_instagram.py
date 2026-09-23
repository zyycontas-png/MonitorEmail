from playwright.sync_api import sync_playwright

USER_DATA = r"C:\Users\Licyyz\AppData\Local\Microsoft\Edge\User Data\Profile 4"
EMAIL = "teste@tuamaeaquelaursa.com"
URL = "https://www.instagram.com/accounts/password/reset/?hl=pt-br"

with sync_playwright() as p:

    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA,
        channel="msedge",
        headless=False
    )

    page = context.pages[0]

    print("Navegador abriu")

    page.goto("https://www.instagram.com/accounts/password/reset/?hl=pt-br")

    print("Página carregada")

        # Aguarda o campo aparecer
    campo = page.locator('input[aria-invalid="false"]')
    
    # Digita como um usuário
    campo.click()
    campo.press_sequentially(EMAIL, delay=50)
    campo.press("Tab")

    page.wait_for_timeout(2000)

   # Botão Continuar
    botao_enviar = page.locator(
        'div[role="button"]',
        has_text="Continuar"
    )

    botao_enviar.click()

    print("Botão Continuar clicado!")

    page.wait_for_timeout(5000)

    input("\nENTER para fechar...")

    context.close()