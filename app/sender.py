from flask import render_template, current_app
from threading import Thread
from flask_mail import Message
from . import mail


def send_email(to, message):
    import smtplib, ssl

    port = 465
    email = current_app.config["EMAIL_ADDRESS"]
    password = current_app.config["EMAIL_PASSWORD"]
    if email == "" or password == "":
        return
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, to, message)
