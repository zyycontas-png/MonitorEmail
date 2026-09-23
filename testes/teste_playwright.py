from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    print("[1] Abrindo o site...")
    page.goto("https://tuamaeaquelaursa.com")

    page.wait_for_load_state("networkidle")

    print("[2] Clicando em 'Acessar email'...")
    page.get_by_role("button", name="Acessar email").click()

    page.wait_for_load_state("networkidle")

    page.wait_for_timeout(2000)

    print("[3] Capturando e-mail...")

    email = page.locator("input").input_value()

    print(f"[OK] E-mail encontrado: {email}")

    input("\nPressione ENTER para fechar...")

    browser.close()

print("Teste finalizado.")