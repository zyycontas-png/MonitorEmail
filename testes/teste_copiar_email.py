from playwright.sync_api import sync_playwright
import pyperclip

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    print("[1] Abrindo site...")
    page.goto("https://tuamaeaquelaursa.com")

    page.wait_for_load_state("networkidle")

    print("[2] Clicando em 'Acessar email'...")
    page.get_by_role("button", name="Acessar email").click()

    page.wait_for_load_state("networkidle")

    print("[3] Aguardando carregar a caixa de entrada...")
    page.wait_for_timeout(3000)

    print("[4] Clique manualmente no botão 'Copiar'.")
    input("Depois que copiar, pressione ENTER...")

    print("Email copiado:")
    print(pyperclip.paste())

    browser.close()