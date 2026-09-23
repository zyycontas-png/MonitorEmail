from playwright.sync_api import sync_playwright

USER_DATA = r"C:\Users\Licyyz\AppData\Local\Microsoft\Edge\User Data\Profile 4"
EMAIL = "teste@tuamaeaquelaursa.com"
URL_FORGET = "https://www.instagram.com/accounts/emailsignup/"

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA,
        channel="msedge",
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-infobars"
        ],
        ignore_default_args=["--enable-automation"]
    )

    # 1. Fecha a aba padrão e abre uma nova aba limpa
    aba_inicial = context.pages[0]
    page = context.new_page()
    aba_inicial.close()

    # 2. Aplica Stealth Nativo via Chrome DevTools Protocol (CDP)
    client = page.context.new_cdp_session(page)
    client.send("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['pt-BR', 'pt', 'en-US']});
            window.chrome = { runtime: {} };
        """
    })

    print("Navegador aberto com Stealth Nativo aplicado.")

    # 3. Acessa primeiro a Home para gerar os cookies/tokens orgânicos
    page.goto("https://www.tiktok.com", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)

    # 4. Navega para a página de redefinição
    page.goto(URL_FORGET, wait_until="networkidle")
    print("Página de redefinição carregada.")

    # 5. Localiza e interage com o campo de e-mail
    campo = page.locator('input[name="email"]')
    campo.wait_for(state="visible")

    box_campo = campo.bounding_box()
    if box_campo:
        page.mouse.move(box_campo["x"] + 10, box_campo["y"] + 10)
        page.mouse.click(box_campo["x"] + 10, box_campo["y"] + 10)

    campo.press_sequentially(EMAIL, delay=120)
    page.wait_for_timeout(1500)

    # 6. Clica no botão "Enviar código" simulando clique físico de mouse
    botao_enviar = page.locator('button[data-e2e="send-code-button"]')
    botao_enviar.wait_for(state="visible")

    box_botao = botao_enviar.bounding_box()
    if box_botao:
        page.mouse.move(box_botao["x"] + box_botao["width"] / 2, box_botao["y"] + box_botao["height"] / 2)
        page.wait_for_timeout(500)
        page.mouse.down()
        page.wait_for_timeout(100)
        page.mouse.up()
        print("Clique físico executado no botão!")

    input("\nENTER no terminal para finalizar...")
    context.close()