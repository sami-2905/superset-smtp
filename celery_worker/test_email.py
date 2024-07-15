import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Define email parameters
from_email = 'artemis-alerts@omnissa.com'
to_email = 'samiksha.sharma@broadcom.com'
subject = 'Superset SMTP config test'
message = 'It worked'

# Create the email message
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = subject
msg.attach(MIMEText(message))

# Email server configuration
smtp_server = 'email-smtp.us-west-2.amazonaws.com'
smtp_port = 587
username = 'AKIAXDRHV5ZLA5BTZW6T'  # replace with your SMTP username
password = 'BKMS8bybTogsduzAlIMituI03RaFsOmiIE9I71TdkYC0'  # replace with your SMTP password

# Connect to the email server and send the email
try:
    mailserver = smtplib.SMTP(smtp_server, smtp_port)
    mailserver.starttls()  # Enable TLS
    mailserver.login(username, password)  # Login to the email server
    mailserver.sendmail(from_email, to_email, msg.as_string())  # Send the email
    mailserver.quit()
    print('Email sent successfully')
except smtplib.SMTPException as e:
    print('Error sending email:', e)

