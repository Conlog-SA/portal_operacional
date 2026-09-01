from datetime import datetime
import time
import requests
from apps.envio_email_app.views import Envio_Email


# Create your views here.
class Envia_Notificacao_Whats():
    def __init__(self):
        # ── CONFIGURAÇÕES DA EVOLUTION API ───────────────────────────────────────────
        self.EVOLUTION_URL = "https://exorcism-displease-satisfied.ngrok-free.dev"
        self.EVOLUTION_API_KEY = "ChaveDjango456"
        self.EVOLUTION_INSTANCE = "formularios"

    def envia_msg(self, lista_destinos, msg):
        #print('Enviando mensagem')
        """Envia mensagem de texto via Evolution API."""
        url = f"{self.EVOLUTION_URL}/message/sendText/{self.EVOLUTION_INSTANCE}"

        headers = {
            "Content-Type": "application/json",
            "apikey": self.EVOLUTION_API_KEY,
        }

        for destino in lista_destinos:
            payload = {
                "number": destino,
                "text": msg,
            }

            '''print(f"📱 Destino: {destino}")
            print(f"📝 Mensagem: {repr(msg)}")
            print(f"📦 Payload: {payload}")'''

            try:
                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=30
                )

                '''print(f"📊 Status: {response.status_code}")
                print(f"📄 Resposta API: {response.text}")'''

                response.raise_for_status()

                #print(f"✅ WhatsApp enviado com sucesso para {destino}")

            except requests.exceptions.RequestException as e:
                print(f"❌ Erro ao enviar WhatsApp para {destino}: {e}")
                lista_email_cco = ['danilo.costa@conlogsa.com.br', 'juliana.deus@conlogsa.com.br']
                assunto_email = f'Erro Safety envio de Whats'
                corpo_email = f"❌ Erro ao enviar WhatsApp para {destino}: {e}\n{msg}"
                Envio_Email().envia_email_layout_generico_safety_deep(lista_email_cco, assunto_email, corpo_email)

            time.sleep(10)

        return True
