How to run it? 

Run `python3 main.py -h` or `python3 main.py -help` for help.

'message.txt' file should contain the body of your email.

'emails.csv' file should contain First name, Company, Email in that order of each person you want to email.

To reference the first name in the email body use `{first}`. To reference the company name in the email body use `{company}`

You must put quotes around each argument.

Example command line argument:

`gmail_sender % python3 main.py --subject 'Purdue Undergrad - Software Engineering Internship' --resume_path 'AdhikaryParas2020.pdf'`