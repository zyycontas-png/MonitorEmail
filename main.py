import time
from datetime import datetime
from playwright.sync_api import sync_playwright

from email_temp import gerar_email_temporario
from tiktok import (
    iniciar_navegador_tiktok, 
    abrir_tiktok, 
    preencher_email, 
    enviar_codigo, 
    verificar_status_email
)
from telegram_bot import enviar_notificacao_telegram


def salvar_email_valido(email: str):
    """Registra o e-mail válido com data/hora em um arquivo local."""
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("emails_validos.txt", "a", encoding="utf-8") as f:
        f.write(f"[{data_hora}] {email}\n")
    print(f"[ARQUIVO] {email} salvo em 'emails_validos.txt'")


def executar_loop_continuo():
    tentativa = 1

    with sync_playwright() as p:
        while True:
            print("\n" + "=" * 55)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] TENTATIVA #{tentativa}")
            print("=" * 55)

            context_email = None
            context_tiktok = None

            try:
                # 1. Gera o e-mail temporário
                print("[1/4] Gerando e-mail temporário...")
                email_temp, context_email = gerar_email_temporario(p)

                if not email_temp:
                    print("[ERRO] Falha ao obter e-mail. Tentando novamente em 3s...")
                    tentativa += 1
                    time.sleep(3)
                    continue

                print(f"[INFO] E-mail gerado: {email_temp}")

                # 2. Abre o TikTok e realiza os cliques
                print("[2/4] Testando e-mail no TikTok...")
                context_tiktok, page_tiktok = iniciar_navegador_tiktok(p)

                abrir_tiktok(page_tiktok)
                preencher_email(page_tiktok, email_temp)
                enviar_codigo(page_tiktok)

                # 3. Verifica a resposta da página
                print("[3/4] Analisando resultado...")
                eh_valido = verificar_status_email(page_tiktok)

                if eh_valido:
                    print(f"\n🎯 >>> [SUCESSO] {email_temp} É VÁLIDO! <<<")
                    
                    # Salva no .txt e notifica no Telegram
                    salvar_email_valido(email_temp)
                    enviar_notificacao_telegram(email_temp)
                else:
                    print(f"❌ [DESCARTADO] {email_temp} é inválido.")

            except Exception as e:
                print(f"[ERRO NO FLUXO] Falha inesperada durante a tentativa: {e}")

            finally:
                # 4. Fecha as janelas do navegador da tentativa atual para liberar memória
                print("[4/4] Limpando processos da tentativa...")
                if context_tiktok:
                    try:
                        context_tiktok.close()
                    except:
                        pass
                if context_email:
                    try:
                        context_email.close()
                    except:
                        pass

            tentativa += 1
            time.sleep(2)  # Pausa de 2 segundos antes de iniciar o próximo e-mail


if __name__ == "__main__":
    print("[SISTEMA INICIADO] Monitoramento rodando em loop automático.")
    print("Para parar a qualquer momento, pressione CTRL + C no terminal.\n")
    
    try:
        executar_loop_continuo()
    except KeyboardInterrupt:
        print("\n[ENCERRADO] Execução interrompida pelo usuário.")