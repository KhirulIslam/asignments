import pandas as pd
from elasticsearch import Elasticsearch
import logging
import datetime
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from os.path import basename

logging.basicConfig(filename='logfile.log',level=logging.DEBUG)

# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')
data = pd.read_csv("winter_products.csv") 
df = pd.DataFrame(data, columns = ['id', 'product_name'])

client = Elasticsearch(hosts=[os.getenv('ELASTICSEARCH_HOST_IP')])
INDEX_NAME = os.getenv('INDEX_NAME')

smtp_port = os.getenv('25')
smtp_server = os.getenv('SMTP_SERVER')
sender_email = os.getenv('SENDER_EMAIL')
password = os.getenv('SENDER_PASSWORD')
receiver_email = os.getenv('RECIVER_EMAIL')
filename = 'logfile.log'

def send_email():
    body = """\
        Dear concern,
            Please find the attached log file."""
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = COMMASPACE.join(receiver_email)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "INDEXING SUMMARY"

    msg.attach(MIMEText(body))

    try:    
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)

        part.add_header("Content-Disposition",
                        f"attachment; filename= {filename}",)
    except Exception as err:
        logging.error("ERROR ATTACHING FILE", err)

    msg.attach(part)

    try:
        smtpObj = smtplib.SMTP(smtp_server)
        smtpObj.sendmail(sender_email, receiver_email, msg.as_string())  
        logging.info("MAIL SENT TO :"+receiver_email)
    except Exception as err:
        logging.error("ERROR SENDING EMAIL", err)


def create_index(doc_body):
    try:
        response = client.index(
        index = INDEX_NAME,
        doc_type = '_doc',
        id = doc_body['id'],
        body = doc_body,
        request_timeout=45)

        logging.info("indexed successfully:", response)

    except Exception as err:
        logging.error("Elasticsearch index() ERROR:", err)

for index, row in df.iterrows():
    doc_body = {
        "id": row["id"],
        "product_name":row["product_name"],
        "time field": datetime.datetime.now()
        }
    create_index(doc_body)
send_email()