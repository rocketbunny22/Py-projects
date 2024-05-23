import sublist3r
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(sender_email, receiver_email, subject, body, password, smtp_server, port):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        
        server.login(sender_email, password)

        server.sendmail(sender_email, receiver_email, msg.as_string())
        
        print("Scan finished, Email sent with results.")
    except Exception as e:
        print(f"Error: {e}")
    finally: server.quit()
    
    
sender_email = 'noltderek5@gmail.com'
receiver_email = 'derek@viztech360.com'
subject = 'Subdomain Enumeration results'

password = 'kdlv iveh hvdg uuil ' 
smtp_server = 'smtp.gmail.com'
port = 587  

# Define target domain
domain = "viztech360.com"

# Run sublist3r and store the results in a variable
subdomains = sublist3r.main(domain, enable_bruteforce=False, engines=None, threads=1, savefile=None, ports=None, silent=True, verbose=False)

body = "\n".join(subdomains)

if body:
 send_email(sender_email, receiver_email, subject, body, password, smtp_server, port)
else:
    print('Scan failed')
