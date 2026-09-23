from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://www.instagram.com/accounts/emailsignup/")

    page.wait_for_load_state("networkidle")

   
    page.wait_for_load_state("networkidle")

    page.wait_for_timeout(3000)

    inputs = page.locator("input")

    print(f"Total de inputs: {inputs.count()}")

    for i in range(inputs.count()):
        print("----------------------")
        print("INPUT", i)
        print(inputs.nth(i).input_value())

    input("ENTER para fechar")

    browser.close()