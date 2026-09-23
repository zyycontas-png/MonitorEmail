USER_DATA = r"C:\Users\Licyyz\AppData\Local\Microsoft\Edge\User Data\Profile 4"
URL_FORGET = "https://www.tiktok.com/login/email/forget-password"


def iniciar_navegador_tiktok(playwright):
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=USER_DATA,
        channel="msedge",
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-infobars",
            "--autoplay-policy=user-gesture-required",  # Impede os vídeos de tocar/carregar automaticamente
            "--mute-audio"                               # Silencia o áudio
        ],
        ignore_default_args=["--enable-automation"]
    )

    aba_inicial = context.pages[0]
    page = context.new_page()
    aba_inicial.close()

    # Aplica Stealth Nativo via CDP
    client = page.context.new_cdp_session(page)
    client.send("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['pt-BR', 'pt', 'en-US']});
            window.chrome = { runtime: {} };
        """
    })

    print("[INFO] Navegador do TikTok aberto com Stealth.")
    return context, page


def abrir_tiktok(page):
    # Vai direto para a página de redefinição para economizar tempo
    page.goto(URL_FORGET, wait_until="domcontentloaded")
    print("[INFO] Página de redefinição carregada.")


def preencher_email(page, email):
    campo = page.locator('input[name="email"]')
    campo.wait_for(state="visible")

    box_campo = campo.bounding_box()
    if box_campo:
        page.mouse.move(box_campo["x"] + 10, box_campo["y"] + 10)
        page.mouse.click(box_campo["x"] + 10, box_campo["y"] + 10)

    campo.press_sequentially(email, delay=120)
    page.wait_for_timeout(1000)



def enviar_codigo(page):
    botao_enviar = page.locator('button[data-e2e="send-code-button"]')
    botao_enviar.wait_for(state="visible")

    box_botao = botao_enviar.bounding_box()
    if box_botao:
        page.mouse.move(box_botao["x"] + box_botao["width"] / 2, box_botao["y"] + box_botao["height"] / 2)
        page.wait_for_timeout(300)
        page.mouse.click(box_botao["x"] + box_botao["width"] / 2, box_botao["y"] + box_botao["height"] / 2)
        print("[INFO] Botão clicado!")


def verificar_status_email(page) -> bool:
    """
    Aguarda e verifica se o e-mail é válido ou não no TikTok.
    Retorna True para VÁLIDO e False para INVÁLIDO.
    """
    print("[INFO] Aguardando resposta do TikTok...")

    # .filter(has_text=...) garante que pegamos apenas o span que possui o texto de erro
    locator_erro = page.locator('span[role="status"]').filter(has_text="não está")
    locator_botao = page.locator('button[data-e2e="send-code-button"]').first

    for _ in range(12):
        # 1. CASO INVÁLIDO: Mensagem de erro visível
        if locator_erro.count() > 0 and locator_erro.first.is_visible():
            print("❌ [INVALIDO] O e-mail não está registrado no TikTok.")
            return False

        # 2. CASO VÁLIDO: Botão alterado para 'Reenviar código'
        if locator_botao.is_visible():
            texto_botao = locator_botao.inner_text().lower()
            if "reenviar" in texto_botao:
                print("✅ [VALIDO] E-mail registrado! Código enviado com sucesso.")
                return True

        page.wait_for_timeout(500)

    print("⚠️ [AVISO] Tempo limite atingido sem confirmação.")
    return False