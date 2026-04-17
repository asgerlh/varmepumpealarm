import umail
from config import mail

def send_mail():
    smtp = umail.SMTP('smtp.gmail.com', 587)
    smtp.login(mail.sender, mail.password)
    smtp.to(mail.recipient)
    smtp.send("Subject: Varmepumpealarm\n\nDer er et problem med varmepumpen. Tjek app'en.")
    smtp.quit()
