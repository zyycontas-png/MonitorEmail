from playwright.sync_api import sync_playwright


URL = "https://www.instagram.com/accounts/emailsignup/"


def encontrar_elementos_clicaveis(page):

    print("\n===== ELEMENTOS CLICÁVEIS ENCONTRADOS =====\n")

    elementos = page.locator(
        "button, [role='button'], a, input[type='submit'], div[role='button']"
    )

    total = elementos.count()

    print(f"Total encontrado: {total}\n")

    for i in range(total):

        el = elementos.nth(i)

        print(f"\nELEMENTO {i+1}")
        print("----------------------------")

        try:
            print("Tag:",
                  el.evaluate("(e)=>e.tagName"))
        except:
            pass

        try:
            texto = el.inner_text(timeout=1000).strip()
            print("Texto:", texto)
        except:
            print("Texto: [vazio]")

        print("ID:",
              el.get_attribute("id"))

        print("Classe:",
              el.get_attribute("class"))

        print("Role:",
              el.get_attribute("role"))

        print("Name:",
              el.get_attribute("name"))

        print("Type:",
              el.get_attribute("type"))

        try:
            html = el.evaluate("(e)=>e.outerHTML")
            print("HTML:")
            print(html[:500])
        except:
            pass

        print("----------------------------")


with sync_playwright() as p:

    navegador = p.chromium.launch(
        headless=False
    )

    pagina = navegador.new_page()

    print("Abrindo Instagram...")
    pagina.goto(URL)

    print("Esperando carregar...")
    pagina.wait_for_timeout(8000)

    encontrar_elementos_clicaveis(pagina)

    input("\nENTER para fechar...")

    navegador.close()