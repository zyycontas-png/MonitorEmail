from playwright.sync_api import sync_playwright

USER_DATA = r"C:\Users\Licyyz\AppData\Local\Microsoft\Edge\User Data\Profile 4"

with sync_playwright() as p:

    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA,
        channel="msedge",
        headless=False
    )

    page = context.pages[0]

    print("Navegador abriu")

    page.goto("https://www.tiktok.com/login/email/forget-password")

    print("Página carregada")

    input("ENTER para fechar...")