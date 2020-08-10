from __future__ import print_function
import pickle
import os.path
import base64
import csv
import argparse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def create_message_with_attachment(sender, to, subject, message_text, file):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    filename = os.path.basename(file)
    with open(filename, "rb") as f:
        msg = MIMEApplication(f.read(), _subtype="pdf")
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {'raw': raw_message.decode("utf-8")}


def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        print('Message Sent!')
        return message
    except Exception as e:
        print('An error occurred: %s' % e)
        return None


def main(subject, resume_path):
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=3000)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    with open('message.txt') as fil:
        body = fil.read()

    recruiters = list()
    with open('emails.csv', newline='') as csvfile:
        emails = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in emails:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                # print(f'\t{row[0]} works at {row[1]}, their email is {row[2]}.')
                recruiters.extend([row])
                line_count += 1
        print(f'Processed {line_count} lines.')

    for r in recruiters:
        temp = f'{body}'
        temp = temp.replace('{first}', r[0]).replace('{company}', r[1])
        message = create_message_with_attachment('paras.adhikary@gmail.com', r[2], subject, temp, resume_path)
        send_message(service, 'paras.adhikary@gmail.com', message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This program allows you to send multiple emails to different people using the Gmail API')
    parser.add_argument("--subject", help="Subject line of email, i.e. 'Purdue Undergrad - Software Engineering Internship'", required=True)
    parser.add_argument("--resume_path", help="Name of resume file in the directory, i.e. 'AdhikaryParas2020.pdf'", required=True)
    args = parser.parse_args()
    main(subject=args.subject, resume_path=args.resume_path)
