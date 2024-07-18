from groq import Groq
from config import groq_api_key
import pandas as pd
import fpdf

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
            # All models: llama3-8b-8192 llama3-70b-8192 gemma-7b-it mixtral-8x7b-32768
            temperature = self.temperature,
            top_p=self.top_p)

        return chat_completion.choices[0].message.content

def extract_from_spreadsheet(sheet_link):
    df = pd.read_csv(sheet_link)
    # print(df.describe())
    # print(df.info())
    return df

def convert_to_pdf(string):

    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 5, txt=string)
    pdf.output("output.pdf", "F")