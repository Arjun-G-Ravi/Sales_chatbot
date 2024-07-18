import re
from helper import LLM, extract_from_spreadsheet, convert_to_pdf, custom_information_extraction, schedule_email
import time
import os
import schedule
import datetime

current_time = time.strftime("%H:%M")

prompt = f'''You are a chatbot designed to classify the input text into multiple tasks.
- If the text is to summarise the content of any file, your output should contain [FILE].
- If the text is to sent an email, your output should be [EMAIL].
- If the text is to sent an email at a particular time, your output should be [EMAIL][TIME-<actual time to send the email from prompt>]
- If it is any other regular question, just answer the question.
The current time is {current_time}.
Human:'''

llm = LLM()

while True:
    inp = input('You: ')
    output = llm.generate(prompt + inp)
    print('Chatbot:', output, '\n')
    if re.search(r'\[FILE\]', output):
        # print('file found')
        file_path = input("Enter file path: ")
        if os.path.exists(file_path):
            df = extract_from_spreadsheet(file_path)
            information = custom_information_extraction(df)
            output = llm.generate( 'You are given the following details about the sales of a company. Write a very long sales report on the same. All the money shown are in indian rupees(use Rs). Answer in only english text format(not markdown).Do not add any charts. Make sure to arrange the report with proper headings.'+ str(information))
            convert_to_pdf(output)
        else: break

    if re.search(r'\[EMAIL\]', output):
        match = re.search(r'\[TIME-(\d{2}:\d{2})\]', output)
        if match:
            schedule_time = match.group(1)
        else:
            schedule_time = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%H:%M")

        schedule.every().day.at(schedule_time).do(schedule_email)

        print(f'Scheduled email to be sent at {schedule_time}')

        while True:
            schedule.run_pending()
            time.sleep(1)