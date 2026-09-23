EMAIL_GERADOR_URL = "https://tuamaeaquelaursa.com"


def gerar_email_temporario(playwright):
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=r"C:\Users\Licyyz\AppData\Local\Google\Chrome\User Data\PlaywrightProfile",
        channel="chrome",
        headless=False
    )

    page = context.pages[0] if context.pages else context.new_page()

    try:
        print("[...] Acessando gerador de e-mail...")
        page.goto(EMAIL_GERADOR_URL, wait_until="domcontentloaded")

        print("[...] Clicando no botão 'Acessar'...")
        btn_acessar = page.locator("button.access-submit")
        btn_acessar.wait_for(state="visible", timeout=10000)
        btn_acessar.click()

        print("[...] Aguardando input do e-mail...")
        input_locator = page.locator("input#evolution-mailbox-compact")
        input_locator.wait_for(state="visible", timeout=15000)

        page.wait_for_function(
            "el => el && el.value.trim() !== ''",
            arg=input_locator.element_handle(),
            timeout=10000
        )

        prefixo_email = input_locator.input_value()
        email_completo = prefixo_email if "@" in prefixo_email else f"{prefixo_email}@tuamaeaquelaursa.com"

        print(f"[OK] Email gerado: {email_completo}")
        return email_completo, context

    except Exception as e:
        print(f"[ERRO] Gerador: {e}")
        return None, context