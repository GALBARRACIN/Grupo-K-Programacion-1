from ..mail import mailsender  # Importa la instancia de Flask-Mail definida en __init__.py
from flask import current_app, render_template
from flask_mail import Message
from smtplib import SMTPException

def sendMail(to, subject, template, **kwargs):
    """
    Envía un correo utilizando Flask-Mail.

    Parámetros:
        to: Dirección de correo del destinatario o lista de direcciones.
        subject: Asunto del correo.
        template: Nombre base de la plantilla (sin extensión) que se usará para renderizar el mail.
        **kwargs: Variables para renderizar la plantilla, por ejemplo, {'usuario': usuario}.

    La función renderiza las plantillas para el cuerpo en formato texto (.txt) y HTML (.html) y envía el correo.
    """
    msg = Message(
        subject,
        sender=current_app.config['FLASKY_MAIL_SENDER'],
        recipients=to if isinstance(to, list) else [to]
    )
    try:
        # Renderiza las plantillas para texto y HTML
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mailsender.send(msg)
    except SMTPException as e:
        print(str(e))
        return "Mail delivery failed"
    return True
