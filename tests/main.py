import pandas as pd
import re
from helper import LLM, extract_from_spreadsheet, convert_to_pdf

prompt = '''You are a chatbot designed to classify the input text into multiple tasks.
- If the text is to summarise the content of any file, your output should contain [FILE].
- If the text is to generate an email, your output should be [EMAIL].
- If it is any other regular question, just answer the question.

Human:'''


llm = LLM()

# path = 'Sample Sales Data- Interns task - sales_data_sample.csv'

# spread_sheet_info = extract_from_spreadsheet(path)

# sales_summary = llm.generate(f'summarise this dataframe {spread_sheet_info}')
# convert_to_pdf(sales_summary)

while True:
    inp = input('H: ')
    # print(prompt + inp)
    output = llm.generate(prompt + inp)
    print(output, '\n')