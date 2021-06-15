import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from io import StringIO
import logging

class EmailServer():

    def __init__(self, recipient_list):
        self.recipient_list = recipient_list
        # set up domains
        self.smtp_host = 'smtp.gmail.com'
        self.smtp_port = 587
        self.smtp_user = 'yourEmailAddressHere@gmail.com'
        self.smtp_password = 'youPasswordHere'
        self.server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.smtp_user, self.smtp_password)

    def send(self,subject,message,recipient_list=None,mock=True):
        ''' Send email with message in html format '''
        if recipient_list is None:
            recipient_list = self.recipient_list
        for recipient in recipient_list:
            # email content set up
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = self.smtp_user
            msg['To'] = recipient
            msg.add_header('Content-Type','text/html')
            msg.attach(MIMEText(message, 'html'))
            if mock:
                logging.info('Mock: Sent to {}'.format(recipient))
            else:
                self.server.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))       
                logging.info('Sent to {}'.format(recipient))

    def send_csv_attachment(self,subject,message,filename,df,recipient_list=None,mock=True):
        ''' Send email with df saved as the csv file in attachment '''
        if recipient_list is None:
            recipient_list = self.recipient_list
        for recipient in recipient_list:
            # email content set up
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = self.smtp_user
            msg['To'] = recipient
            msg.add_header('Content-Type','text/html')
            msg.attach(MIMEText(message, 'html'))
            textStream = StringIO()
            df.to_csv(textStream,index=False)
            msg.attach(MIMEApplication(textStream.getvalue(), Name=filename))
            if mock:
                logging.info('Mock: Sent to {}'.format(recipient))
            else:
                self.server.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))       
                logging.info('Sent to {}'.format(recipient))

