# -*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

GMAIL_ACCOUNT = "지메일 계정"
GMAIL_PASSWRD = "비밀번호"


# 지메일 SMTP 서버를 통해 메일을 발송한다.
# to_addr - 수신자 메일 주소 배열
# title - 메일 제목
# description - 메일 본문
# image_file - 첨부할 이미지 파일명
def send_via_gmail(to_addr, title, description, image_file=None):
    msg = get_message_formatted(GMAIL_ACCOUNT, to_addr, title, description, image_file)

    try:
        s = smtplib.SMTP('smtp.gmail.com:587')  # port 465 or 587
        s.starttls()
        s.login(GMAIL_ACCOUNT, GMAIL_PASSWRD)
        s.sendmail(GMAIL_ACCOUNT, to_addr, msg.as_string())
        s.quit()
    except:
        print "error: failed to send a mail"


# 메일 프로토콜에 맞는 메일 메세지를 생성한다.
def get_message_formatted(from_addr, to_addr, title, description, image_file):
    msg = MIMEMultipart('localhost')
    msg['Subject'] = title
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addr)

    content = MIMEText(description, 'plain', _charset="utf-8")
    msg.attach(content)

    if image_file is not None:
        fp = open(image_file, 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)

    return msg


send_via_gmail([GMAIL_ACCOUNT], "테스트 메일 제목 입니다.", "테스트 메일 본문 내용 입니다.", "baby2.jpg")