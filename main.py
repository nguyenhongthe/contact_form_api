import os
import arrow

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn

load_dotenv()

# Khởi tạo FastAPI
app = FastAPI(
    title="Contact Form API",
    description="This is FastAPI-based API is designed for submitting contact forms and receiving notifications.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    terms_of_service="https://nguyenhongthe.net/tos/",
    contact={
        "name": "Nguyen Hong The",
        "url": "https://nguyenhongthe.dev/contact/",
        "email": "hello@nguyenhongthe.dev",
    },
    license_info={
        "name": "MIT License",
        "url": "https://nguyenhongthe.net/license/"
    },
)


# Cấu hình chung
class Settings(BaseSettings):
    postgres_url: str = os.getenv('POSTGRES_URL') # Đường dẫn kết nối cơ sở dữ liệu PostgreSQL
    discord_webhook_url: str = os.getenv('DISCORD_WEBHOOK_URL') # Đường dẫn webhook Discord để nhận thông báo
    sender_name: str = os.getenv('SENDER_NAME') # Tên người gửi (Tên của website)
    sender_email: str = os.getenv('SENDER_EMAIL') # Địa chỉ email dùng để gửi thông báo khi người dùng gửi form
    recipient_name: str = os.getenv('RECIPIENT_NAME') # Tên người nhận thông báo khi người dùng gửi form
    recipient_email: str = os.getenv('RECIPIENT_EMAIL') # Địa chỉ email nhận thông báo khi người dùng gửi form
    smtp_server: str = os.getenv('SMTP_SERVER') # SMTP server
    smtp_port: int = int(os.getenv('SMTP_PORT')) # SMTP port
    smtp_username: str = os.getenv('SMTP_USERNAME') # SMTP username
    smtp_password: str = os.getenv('SMTP_PASSWORD') # SMTP password

# Danh sách url được phép gọi API, thêm bất kỳ URL nào bạn muốn cho phép gọi API, giúp tránh lỗi CORS
    origins_urls: list = [
        os.getenv(f'ORIGINS_URL_{i+1}') for i in range(8) 
        if os.getenv(f'ORIGINS_URL_{i+1}')
    ]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
sender_name = settings.sender_name

# Cấu hình middleware cho phép CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_urls,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cấu hình SQLAlchemy
SQLALCHEMY_DATABASE_URL = settings.postgres_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Chuyển đổi thời gian sang định dạng chuẩn ISO 8601 (YYYY-MM-DD HH:mm:ss) và có múi giờ GMT+7 để lưu vào database
created_at = arrow.utcnow().to('Asia/Ho_Chi_Minh').format('YYYY-MM-DD HH:mm:ss')


# Tạo cơ sở dữ liệu
class ContactForm(Base):
    __tablename__ = "contact_forms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String)
    title = Column(String)
    message = Column(String)
    created_at = Column(String, default=created_at)


Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    """
    fake root
    """
    return {"message": "Hello World"}

@app.get("/api")
async def api():
    """
    fake api
    """
    return {"message": "Hello API"}

@app.post("/submit-contact-form")
async def submit_contact_form(
        name: str = Form(...),
        email: str = Form(...),
        phone: str = Form(...),
        title: str = Form(...),
        message: str = Form(...),
):
    """
    API gửi form liên hệ
    """
    print("Dữ liệu nhận được từ form:")
    print("Tên:", name)
    print("Email:", email)
    print("Số điện thoại:", phone)
    print("Tiêu đề:", title)
    print("Lời nhắn:", message)
    print("Gửi lúc:", created_at)

    # Lưu dữ liệu vào database
    db = SessionLocal()
    db_contact_form = ContactForm(name=name, email=email, phone=phone, title=title, message=message, created_at=created_at)
    db.add(db_contact_form)
    db.commit()
    db.refresh(db_contact_form)

    # Gửi thông báo qua Discord webhook
    discord_message = f"[{sender_name}] New contact form submission:\n\n *Time: {created_at}*\n\n- Name: {name}\n- Email: {email}\n- Phone: {phone}\n- Title: {title}\n- Message:\n\n{message}"
    send_discord_notification(discord_message)

    # Gửi email thông báo
    email_subject = f"[{sender_name}] New Contact Form Submission"
    email_message = f"[{sender_name}] New Contact Form Submission\n\n *Time: {created_at}*\n\n- Name: {name}\n- Email: {email}\n- Phone: {phone}\n- Title: {title}\n- Message:\n\n{message}"
    reply_to_name = name
    reply_to_email = email
    send_email(sender_name, email_subject, email_message, reply_to_name, reply_to_email)

    return {"success": True, "message": "Form submitted successfully"}

# Hàm gửi thông báo qua Discord webhook
def send_discord_notification(message):
    """
    Gửi thông báo qua Discord webhook
    """
    data = {
        "content": message
    }
    with httpx.Client() as client:
        response = client.post(settings.discord_webhook_url, json=data)
        if response.status_code == 204:
            return True
        return False

# Hàm gửi email thông báo
def send_email(sender_name, subject, message, reply_to_name, reply_to_email):
    """
    Gửi email thông báo
    :param sender_name: Tên người gửi (Tên của website)
    :param sender_email: Địa chỉ email người gửi (Địa chỉ email dùng để gửi thông báo khi người dùng gửi form)
    :param recipient_name: Tên người nhận thông báo
    :param recipient_email: Địa chỉ email dùng để nhận thông báo khi người dùng gửi form
    :param subject: Tiêu đề email
    :param message: Nội dung email
    :param reply_to_name: Tên người gửi form (Tên người dùng nhập vào form)
    :param reply_to_email: Địa chỉ email người gửi form (Địa chỉ email người dùng nhập vào form)
    :param return: True nếu gửi thành công, False nếu gửi thất bại
    """
    msg = MIMEMultipart()
    msg["From"] = f"{sender_name} <{settings.sender_email}>"
    msg["To"] = f"{settings.recipient_name} <{settings.recipient_email}>"
    msg["Subject"] = subject
    msg["Reply-To"] = f"{reply_to_name} <{reply_to_email}>"

    body = MIMEText(message, "plain", "utf-8")
    msg.attach(body)

    try:
        server = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        server.sendmail(
            settings.sender_email, 
            settings.recipient_email,
              msg.as_string()
              )
        server.quit()
        return True
    except Exception as e:
        print("Email sending failed:", str(e))
        return False


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
