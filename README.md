# Sales_chatbot
A chatbot that summarizes a spreadsheet and emails it to a email address

# Installation
Use `pip install -r requirements.txt` to install the required libraries.

# Setting up the configuration
For the chatbot to work, you would have to create a file called config.py inside the sales_chatbot directory. Now copy paste the following into the file.

```
groq_api_key = 'put your grok api key here'
mail_password = 'the app password for senders mail available at https://myaccount.google.com/apppasswords?pli=1&rapt=AEjHL4NNAGkfLrggOK-ipsCFwYa6vGKw3qylO3PtTbBNH12Cob0mzAnCZvxnUZx7qob9RGDZHFVmF5h_38nqb9OKVC7s2EFV16Us--wPel7QJ8YXnxDpeWE'
sender = 'sender mail id'
receiver = 'reciever mail id'
```

Now modify this file with your information.