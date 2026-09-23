from telegram_bot import enviar_notificacao_telegram

if __name__ == "__main__":
    email_teste = "teste_sucesso@email.com"
    print(f"[TESTE] Enviando mensagem de teste para o Telegram...")
    
    sucesso = enviar_notificacao_telegram(email_teste)
    
    if sucesso:
        print("🚀 [TESTE OK] Verifique se a mensagem chegou no seu aplicativo do Telegram!")
    else:
        print("❌ [FALHA] Ocorreu um erro no envio. Verifique o Token e o Chat ID.")