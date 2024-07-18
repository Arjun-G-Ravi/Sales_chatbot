import pandas as pd
import re
from helper import LLM, extract_from_spreadsheet, convert_to_pdf, custom_information_extraction
import os

prompt = '''You are a chatbot designed to classify the input text into multiple tasks.
- If the text is to summarise the content of any file, your output should contain [FILE].
- If the text is to sent into an email, your output should be [EMAIL].
- If it is any other regular question, just answer the question.

Human:'''

llm = LLM()

while True:
    inp = input('Human: ')
    # print(prompt + inp)
    output = llm.generate(prompt + inp)
    print('Chatbot:', output, '\n')
    if re.search(r'\[FILE\]', output):
        print('file found')
        file_path = input("Enter file path: ")
        if os.path.exists(file_path):
            df = extract_from_spreadsheet(file_path)
            information = custom_information_extraction(df)
            print(information)
            output = llm.generate( 'You are given the following details about the sales of a company. Write a very long sales report on the same. All the money shown are in indian rupees(use Rs). Answer in only english text format(not markdown).Do not add any charts. Make sure to arrange the report with proper headings.'+ str(information))
            print('---------------------')
            print(output)
            print('---------------------')
            convert_to_pdf(output)
        

        else: break



    if re.search(r'\[EMAIL\]', output):
        print('email found')
    
