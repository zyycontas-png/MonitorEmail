import json
import urllib.request

TELEGRAM_TOKEN = "8825671882:AAFqT_2MC79YustkibUSke9L-PqfXysyx2E"
TELEGRAM_CHAT_ID = "8923010817"


def enviar_notificacao_telegram(email: str) -> bool:
    """Envia o e-mail validado para o Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"🎯 *E-mail Válido Encontrado!*\n\n📧 `{email}`",
        "parse_mode": "Markdown"
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, 
            data=data, 
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("[TELEGRAM] Notificação enviada com sucesso!")
                return True
    except Exception as e:
        print(f"[ERRO TELEGRAM] Falha ao enviar mensagem: {e}")
        
    return False