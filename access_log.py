import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEBase
from email.mime.text import MIMEText
from email import encoders

password = "azzura01"
emailAddressFrom = "robin.harris@ayelandsassociates.co.uk"
emailAddressTo = "robin.harris@ayelandsassociates.co.uk"

def printError(problem):
    print(problem)
    print(type(problem))

try:
    received = str(subprocess.check_output('grep Invalid /var/log/auth.log', shell=True))
except Exception as e:
    printError(e)
    received = 'No matches found'

output = bytes(received, "utf-8").decode("unicode_escape")

with open ("failed.txt", "w") as f:
    f.write(output[2:-1])

try:
    received = str(subprocess.check_output('grep Accepted /var/log/auth.log', shell=True))
except Exception as e:
    printError(e)
    received = 'No matches found'

output = bytes(received, "utf-8").decode("unicode_escape")

try:
    with open ("accepted.txt", "w") as f:
        f.write(output[2:-1])
except Exception as e:
    printError(e)


msg = MIMEMultipart()
msg['From'] = emailAddressFrom
msg['To:'] = emailAddressTo
msg['Subject'] = "Daily RPi Log"
body = "Auth.log file extracts"

with open('failed.txt', 'r') as fa:
    att1 = MIMEBase('application', "octet-stream")
    att1.set_payload(fa.read())
    encoders.encode_base64(att1)
    att1.add_header('Content-Disposition', 'attachment', filename='failed.txt')

with open('accepted.txt', 'r') as fb:
    att2 = MIMEBase('application', "octet-stream")
    att2.set_payload(fb.read())
    encoders.encode_base64(att2)
    att2.add_header('Content-Disposition', 'attachment', filename='accepted.txt')
 
msg.attach(att1)    
msg.attach(att2)    
msg.attach(MIMEText(body, 'plain'))
server.ehlo
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(emailAddressFrom, password)
text = msg.as_string()
server.sendmail(emailAddressFrom, emailAddressTo, text)
server.quit()


