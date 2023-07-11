from pathlib import Path

import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List


class EmailSchema(BaseModel):
    email: EmailStr


conf = ConnectionConfig(
    MAIL_USERNAME="example@meta.ua",
    MAIL_PASSWORD="secretPassword",
    MAIL_FROM="example@meta.ua",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.meta.ua",
    MAIL_FROM_NAME="Example email",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)

app = FastAPI()


@app.post("/send-email")
async def send_in_background(background_tasks: BackgroundTasks, body: EmailSchema):
    """
    The send_in_background function sends an email in the background.
        It uses a BackgroundTasks object to add a task that will be run in the background.
        The function returns immediately, and does not wait for the email to be sent.
    
    :param background_tasks: BackgroundTasks: Add a task to the background tasks queue
    :param body: EmailSchema: Get the email address from the request body
    :return: {&quot;message&quot;: &quot;email has been sent&quot;}
    :doc-author: Trelent
    """
    
    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=[body.email],
        template_body={"fullname": "Billy Jones"},
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message, template_name="example_email.html")

    return {"message": "email has been sent"}


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)
    