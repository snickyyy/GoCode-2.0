from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from config.settings import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.EMAILS.MAIL_USERNAME,
    MAIL_PASSWORD=settings.EMAILS.MAIL_PASSWORD,
    MAIL_FROM=settings.EMAILS.MAIL_FROM,
    MAIL_PORT=settings.EMAILS.MAIL_PORT,
    MAIL_SERVER=settings.EMAILS.MAIL_SERVER,
    MAIL_FROM_NAME=settings.EMAILS.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.EMAILS.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.EMAILS.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.EMAILS.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.EMAILS.VALIDATE_CERTS
)

async def send_email(email, token, username=""):
    html = f"""<p>Hi {username} this registration mail, thanks for using GoCode<br><a href="http://{settings.HOST}/accounts/auth/activate-account/{token}" </p> """

    message = MessageSchema(
        subject="GoCode confirm account",
        recipients=[email],
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message":"good"}
