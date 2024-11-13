import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random


email_address = "heyzystudio@gmail.com"
email_password = "ceagjrkviypkiczv"  


def email_yuborish(qabul_qiluvchi_email, mavzu, matn):
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = qabul_qiluvchi_email
    msg['Subject'] = mavzu

    # Xabar matni qo'shish
    msg.attach(MIMEText(matn, 'plain'))

    # Gmail SMTP serveriga ulanish
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Xavfsiz ulanish
        server.login(email_address, email_password)
        text = msg.as_string()
        server.sendmail(email_address, qabul_qiluvchi_email, text)
        print("Email yuborildi!")
    except Exception as e:
        print(f"Xato yuz berdi: {e}")
    finally:
        server.quit()



def generate_confirm_code():
    characters = "0123456789"
    code = ''.join(random.choices(characters, k=4))
    return int(code)
