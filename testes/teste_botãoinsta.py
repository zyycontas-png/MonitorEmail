from playwright.sync_api import sync_playwright


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(
        "https://www.instagram.com/accounts/emailsignup/"
    )

    # DIA
    page.get_by_role(
        "combobox",
        name="Selecionar o dia"
    ).locator("svg").click()

    page.get_by_text(
        "15",
        exact=True
    ).click()

    # MÊS
    page.get_by_label(
        "Selecionar o mês"
    ).locator("div").filter(
        has_text="Mês"
    ).click()

    page.get_by_text(
        "janeiro",
        exact=True
    ).click()

    # ANO
    page.get_by_label(
        "Selecionar o ano"
    ).locator("div").filter(
        has_text="Ano"
    ).click()

    page.get_by_text(
        "2001",
        exact=True
    ).click()

    print("OK - Data 15/01/2001 preenchida!")

    input("\nPressione ENTER para fechar...")

    browser.close()