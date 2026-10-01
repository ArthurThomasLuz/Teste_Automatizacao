import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests


def obter_cotacao_dolar():
    # Consulta a API pública da AwesomeAPI para obter a cotação USD -> BRL
    url = "https://economia.awesomeapi.com.br/last/USD-BRL"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        cotacao = float(dados["USDBRL"]["bid"])
        var = dados["USDBRL"]["pctChange"]
        return f"R$ {cotacao:.2f} (Variação no dia: {var}%)"
    else:
        raise Exception("Erro ao consultar a API do dólar.")


def enviar_email(valor_dolar):
    remetente = os.environ.get("EMAIL_REMETENTE")
    senha = os.environ.get("EMAIL_SENHA")
    destinatario = os.environ.get("EMAIL_DESTINATARIO")

    # Configuração da mensagem de e-mail
    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = f"💵 Cotação do Dólar Hoje: {valor_dolar}"

    corpo = f"""
    <h2>Cotação do Dólar</h2>
    <p>Olá!</p>
    <p>O valor atual do dólar retornado ao meio-dia é <strong>{valor_dolar}</strong>.</p>
    <br>
    <p><small>Enviado automaticamente via GitHub Actions.</small></p>
    """
    msg.attach(MIMEText(corpo, "html"))

    # Envio através do servidor SMTP do Gmail
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(remetente, senha)
    servidor.sendmail(remetente, destinatario, msg.as_string())
    servidor.quit()


if __name__ == "__main__":
    dolar = obter_cotacao_dolar()
    enviar_email(dolar)
    print("E-mail enviado com sucesso!")