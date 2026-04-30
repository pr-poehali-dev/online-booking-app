import json
import os
import smtplib
# v2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def handler(event: dict, context) -> dict:
    """Отправляет уведомление о новой записи на почту владельца салона."""

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
    service = body.get("service", "")
    master = body.get("master", "Любой свободный")
    day = body.get("day", "")
    time = body.get("time", "")
    price = body.get("price", "")

    smtp_user = "Siplatova777@list.ru"
    smtp_password = os.environ["SMTP_PASSWORD"]
    to_email = "Siplatova777@list.ru"

    subject = f"Новая запись: {service} — {name}"

    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0f0f19; color: #ffffff; padding: 32px; border-radius: 16px;">
        <div style="background: linear-gradient(135deg, hsl(315,100%,55%), hsl(270,100%,60%)); padding: 2px; border-radius: 14px; margin-bottom: 24px;">
            <div style="background: #0f0f19; border-radius: 12px; padding: 24px; text-align: center;">
                <h1 style="margin: 0; font-size: 24px; font-weight: 700;">Новая запись!</h1>
            </div>
        </div>

        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="padding: 10px 0; color: #888; font-size: 14px; border-bottom: 1px solid #222;">Клиент</td>
                <td style="padding: 10px 0; font-weight: 600; text-align: right; border-bottom: 1px solid #222;">{name}</td>
            </tr>
            <tr>
                <td style="padding: 10px 0; color: #888; font-size: 14px; border-bottom: 1px solid #222;">Телефон</td>
                <td style="padding: 10px 0; font-weight: 600; text-align: right; border-bottom: 1px solid #222;"><a href="tel:{phone}" style="color: hsl(315,100%,65%); text-decoration: none;">{phone}</a></td>
            </tr>
            <tr>
                <td style="padding: 10px 0; color: #888; font-size: 14px; border-bottom: 1px solid #222;">Услуга</td>
                <td style="padding: 10px 0; font-weight: 600; text-align: right; border-bottom: 1px solid #222;">{service}</td>
            </tr>
            <tr>
                <td style="padding: 10px 0; color: #888; font-size: 14px; border-bottom: 1px solid #222;">Мастер</td>
                <td style="padding: 10px 0; font-weight: 600; text-align: right; border-bottom: 1px solid #222;">{master}</td>
            </tr>
            <tr>
                <td style="padding: 10px 0; color: #888; font-size: 14px; border-bottom: 1px solid #222;">Дата и время</td>
                <td style="padding: 10px 0; font-weight: 600; text-align: right; border-bottom: 1px solid #222;">{day} в {time}</td>
            </tr>
            <tr>
                <td style="padding: 10px 0; color: #888; font-size: 14px;">Стоимость</td>
                <td style="padding: 10px 0; font-weight: 700; text-align: right; color: hsl(315,100%,65%); font-size: 18px;">{price} ₽</td>
            </tr>
        </table>

        <div style="margin-top: 24px; padding: 16px; background: rgba(255,255,255,0.04); border-radius: 10px; font-size: 12px; color: #555; text-align: center;">
            Уведомление отправлено автоматически с сайта записи
        </div>
    </div>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.mail.ru", 465) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())

    return {
        "statusCode": 200,
        "headers": cors_headers,
        "body": json.dumps({"ok": True}),
    }