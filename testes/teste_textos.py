from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://tuamaeaquelaursa.com")

    page.wait_for_load_state("networkidle")

    page.get_by_role("button", name="Acessar email").click()

    page.wait_for_load_state("networkidle")

    page.wait_for_timeout(3000)

    print("=" * 50)

    textos = page.locator("body").inner_text()

    print(textos)

    print("=" * 50)

    input("ENTER para fechar...")

    browser.close()