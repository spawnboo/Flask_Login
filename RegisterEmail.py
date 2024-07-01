# coding=utf-8
import secrets
import email.message
import smtplib



# msg=email.message.EmailMessage()
# msg["From"] = "youremail@gmail.com"
# msg["To"]=input("請輸入email: ")
#
# verify_code = ''.join(map(str, random.sample(range(0, 9), 6)))
# print("生成的驗證碼：", verify_code)
#
# msg["Subject"]=f"驗證碼為:{verify_code}"

# 連結郵件伺服器,登入
server=smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login("e01646166@gmail.com", "skqtvprviyrqmmtk")
from_addr = 'e01646166@gmail.com'
to_addr =   'e01646166@hotmail.com'
msg = 'Subject:Python Test mail!!!\n'
msg += 'test mail content'
server.sendmail(from_addr, to_addr, msg, mail_options=(), rcpt_options=())
server.close()

# email_code = input("請輸入驗證碼: ")

# if email_code == verify_code:
#     print("驗證成功")
# else:
#     print("驗證錯誤")