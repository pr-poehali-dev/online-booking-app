import json
import os
import smtplib
# v3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(server, smtp_user, to_email, subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    server.sendmail(smtp_user, to_email, msg.as_string())


def handler(event: dict, context) -> dict:
    """Отправляет уведомление владельцу и подтверждение клиенту о новой записи."""

    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": cors_headers, "body": ""}

    body = json.loads(event.get("body") or "{}")
    name = body.get("name", "")
    phone = body.get("phone", "")
    client_email = body.get("email", "")
    service = body.get("service", "")
    master = body.get("master", "Любой свободный")
    day = body.get("day", "")
    time = body.get("time", "")
    price = body.get("price", "")

    smtp_user = "Siplatova777@list.ru"
    smtp_password = os.environ["SMTP_PASSWORD"]
    owner_email = "Siplatova777@list.ru"

    # Письмо владельцу
    owner_html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0f0f19; color: #ffffff; padding: 32px; border-radius: 16px;">
        <div style="background: linear-gradient(135deg, hsl(315,100%,55%), hsl(270,100%,60%)); padding: 2px; border-radius: 14px; margin-bottom: 24px;">
            <div style="background: #0f0f19; border-radius: 12px; padding: 24px; text-align: center;">
                <h1 style="margin: 0; font-size: 24px; font-weight: 700;">Новая запись!</h1>
            </div>
        </div>
        <table style="width: 100%; border-collapse: collapse;">
            <tr><td style="padding: 10px 0; color: #888; font-size: 14px; border-bottom: 1px solid #222;">Клиент</td><td style="padding: 10px 0; font-weight: 600; text-align: right; border-bottom: 1px solid #222;">{name}</td></tr>
            <tr><td style="padding: 10px 0; color: #888; font-size: 14px; border-bottom: 1px solid #222;">Телефон</td><td style="padding: 10px 0; font-weight: 600; text-align: right; border-bottom: 1px solid #222;"><a href="tel:{phone}" style="color: hsl(315,100%,65%); text-decoration: none;">{phone}</a></td></tr>
            <tr><td style="padding: 10px 0; color: #888; font-size: 14px; border-bottom: 1px solid #222;">Email</td><td style="padding: 10px 0; font-weight: 600; text-align: right; border-bottom: 1px solid #222;">{client_email or "—"}</td></tr>
            <tr><td style="padding: 10px 0; color: #888; font-size: 14px; border-bottom: 1px solid #222;">Услуга</td><td style="padding: 10px 0; font-weight: 600; text-align: right; border-bottom: 1px solid #222;">{service}</td></tr>
            <tr><td style="padding: 10px 0; color: #888; font-size: 14px; border-bottom: 1px solid #222;">Мастер</td><td style="padding: 10px 0; font-weight: 600; text-align: right; border-bottom: 1px solid #222;">{master}</td></tr>
            <tr><td style="padding: 10px 0; color: #888; font-size: 14px; border-bottom: 1px solid #222;">Дата и время</td><td style="padding: 10px 0; font-weight: 600; text-align: right; border-bottom: 1px solid #222;">{day} в {time}</td></tr>
            <tr><td style="padding: 10px 0; color: #888; font-size: 14px;">Стоимость</td><td style="padding: 10px 0; font-weight: 700; text-align: right; color: hsl(315,100%,65%); font-size: 18px;">{price} ₽</td></tr>
        </table>
        <div style="margin-top: 24px; padding: 16px; background: rgba(255,255,255,0.04); border-radius: 10px; font-size: 12px; color: #555; text-align: center;">
            Уведомление отправлено автоматически с сайта записи
        </div>
    </div>
    """

    # Письмо клиенту
    client_html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0f0f19; color: #ffffff; padding: 32px; border-radius: 16px;">
        <div style="background: linear-gradient(135deg, hsl(315,100%,55%), hsl(270,100%,60%)); padding: 2px; border-radius: 14px; margin-bottom: 24px;">
            <div style="background: #0f0f19; border-radius: 12px; padding: 24px; text-align: center;">
                <div style="font-size: 40px; margin-bottom: 8px;">✅</div>
                <h1 style="margin: 0; font-size: 24px; font-weight: 700;">Запись подтверждена!</h1>
                <p style="margin: 8px 0 0; color: #888; font-size: 14px;">Привет, {name}! Ждём тебя</p>
            </div>
        </div>
        <table style="width: 100%; border-collapse: collapse;">
            <tr><td style="padding: 10px 0; color: #888; font-size: 14px; border-bottom: 1px solid #222;">Услуга</td><td style="padding: 10px 0; font-weight: 600; text-align: right; border-bottom: 1px solid #222;">{service}</td></tr>
            <tr><td style="padding: 10px 0; color: #888; font-size: 14px; border-bottom: 1px solid #222;">Мастер</td><td style="padding: 10px 0; font-weight: 600; text-align: right; border-bottom: 1px solid #222;">{master}</td></tr>
            <tr><td style="padding: 10px 0; color: #888; font-size: 14px; border-bottom: 1px solid #222;">Дата и время</td><td style="padding: 10px 0; font-weight: 600; text-align: right; border-bottom: 1px solid #222;">{day} в {time}</td></tr>
            <tr><td style="padding: 10px 0; color: #888; font-size: 14px;">Стоимость</td><td style="padding: 10px 0; font-weight: 700; text-align: right; color: hsl(315,100%,65%); font-size: 18px;">{price} ₽</td></tr>
        </table>
        <div style="margin-top: 24px; padding: 20px; background: rgba(255,80,180,0.08); border: 1px solid rgba(255,80,180,0.2); border-radius: 12px; font-size: 14px; color: #ccc; text-align: center;">
            Если нужно перенести или отменить запись — свяжитесь с нами заранее
        </div>
        <div style="margin-top: 16px; font-size: 12px; color: #444; text-align: center;">
            Это письмо отправлено автоматически, отвечать на него не нужно
        </div>
    </div>
    """

    with smtplib.SMTP_SSL("smtp.mail.ru", 465) as server:
        server.login(smtp_user, smtp_password)
        send_email(server, smtp_user, owner_email, f"Новая запись: {service} — {name}", owner_html)
        if client_email:
            send_email(server, smtp_user, client_email, f"Ваша запись подтверждена — {service}", client_html)

    return {
        "statusCode": 200,
        "headers": cors_headers,
        "body": json.dumps({"ok": True}),
    }
