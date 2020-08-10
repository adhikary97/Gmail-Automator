How to run it? 

Run `python3 main.py -h` or `python3 main.py -help` for help.

'message.txt' file should contain the body of your email.

'emails.csv' file should contain First name, Company, Email in that order of each person you want to email.

To reference the first name in the email body use `{first}`. To reference the company name in the email body use `{company}`

Example of 'credentials.json':
 
 `{"web":{"client_id":"","project_id":"","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"","redirect_uris":["http://localhost:3000"]}}`

You must put quotes around each argument.

Example command line argument:

$ `python3 main.py --email 'your.name@gmail.com' --subject 'Purdue Undergrad - Software Engineering Internship' --resume_path 'AdhikaryParas2020.pdf'`