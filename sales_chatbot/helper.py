from groq import Groq
from config import groq_api_key, mail_password, sender, receiver
import pandas as pd
import fpdf
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class LLM:
    def __init__(self, temperature = 0.2, top_p=0.3):
        self.temperature = temperature
        self.top_p = top_p
        self.client = Groq(api_key=groq_api_key)

    def generate(self, inp):
        '''Generates output using Google API, given the input.'''
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user","content": f"{inp}"}],
            model="llama3-8b-8192",
            # Other models: llama3-8b-8192 llama3-70b-8192 gemma-7b-it mixtral-8x7b-32768
            temperature = self.temperature,
            top_p=self.top_p)

        return chat_completion.choices[0].message.content

def extract_from_spreadsheet(sheet_link):
    df = pd.read_csv(sheet_link)
    return df

def convert_to_pdf(string):
    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(0, 5, txt=string)
    pdf.output("output/output.pdf", "F")


def custom_information_extraction(df):
    '''This function is built on the columns of given spreadsheet'''
    return {
    'sum_QUANTITYORDERED' : sum(df.QUANTITYORDERED),
    'mean_QUANTITYORDERED' : df.QUANTITYORDERED.mean(),
    'sum_PRICEEACH' : sum(df.PRICEEACH),
    'mean_PRICEEACH'  : df.PRICEEACH.mean(),
    'sum_SALES' :sum(df.SALES),
    'mean_SALES'  :df.SALES.mean(),
    'valCounts_STATUS' : df.STATUS.value_counts().to_dict(),
    'sorted_valCounts_MONTHID' : df.MONTH_ID.value_counts().sort_index().to_dict(),
    'sorted_valCounts_YEARID' : df.YEAR_ID.value_counts().sort_index().to_dict(),
    'valCounts_PRODUCTLINE' : df.PRODUCTLINE.value_counts().to_dict(),
    'valCounts_COUNTRY' : df.COUNTRY.value_counts().to_dict(),
    'valCounts_CITY' : df.CITY.value_counts().to_dict(),
    'valCounts_DEALSIZE' : df.DEALSIZE.value_counts().to_dict(),
    }

def send_email(sender_email, receiver_email, subject, body, password, attachment_path):
    global email_sent
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    attachment = open(attachment_path, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={attachment_path.split("/")[-1]}')

    msg.attach(part)
    attachment.close()
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print(f'Email sent successfully.')
    email_sent = True
    quit()

# Function to schedule the email
def schedule_email():
    subject = 'Daily sales'
    body = 'This mail contains an attachment that summarises the daily sales.'
    send_email(sender, receiver, subject, body, mail_password, 'output/output.pdf')
