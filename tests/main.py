import pandas as pd
import re
from helper import LLM, extract_from_spreadsheet, convert_to_pdf


llm = LLM()

path = 'Sample Sales Data- Interns task - sales_data_sample.csv'

spread_sheet_info = extract_from_spreadsheet(path)


sales_summary = llm.generate(f'summarise this dataframe {spread_sheet_info}')


convert_to_pdf(sales_summary)