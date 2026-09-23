from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    print("[1] Abrindo o site...")
    page.goto("https://tuamaeaquelaursa.com")

    # Espera a página carregar
    page.wait_for_load_state("networkidle")

    print("[2] Procurando botão 'Acessar email'...")

    # Clica no botão
    page.get_by_role("button", name="Acessar email").click()

    print("[3] Botão clicado!")

    # Espera a nova página carregar
    page.wait_for_load_state("networkidle")

    print("[4] Caixa de entrada aberta!")

    # Espera alguns segundos para você conferir
    page.wait_for_timeout(10000)

    browser.close()

print("Fim do teste.")