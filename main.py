import pickle
import os
import csv
import smtplib
import ssl
from email.message import EmailMessage
from random import shuffle

from decouple import config

people_csv = 'people.csv'
people_filename = 'people.pkl'
email_template = 'email_template.html'

def get_people_list():
    people = []

    with open(people_csv, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            people.append(row)

    return people

def shuffle_people(people):
    #Check if it has a previus draw
    if not os.path.isfile(people_filename):
        print('New draw, shuffling people...')

        shuffle(people)

        with open(people_filename, 'wb') as pickle_file:
            pickle.dump(people, pickle_file)
        
        return people
    
    with open(people_filename, 'rb') as pickle_file:
        return pickle.load(pickle_file)

def send_mail_from_template(to_email, subject, content):
    try:
        smtp_user = config('EMAIL_LOGIN')
        smtp_password = config('EMAIL_PASSWORD')
        smtp_server = config('SMTP_SERVER')
        sender_address = config('SENDER_ADDRES')
        smtp_port = config('SMTP_PORT', cast=int)

        msg = EmailMessage()
        msg.set_content(content, subtype='html')
        msg['Subject'] = subject
        msg['From'] = f'Amigo Secreto Queiroz <{sender_address}>'
        msg['To'] = to_email

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo() 
            server.starttls(context=context)
            server.ehlo()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

    except Exception as e:
        print(e)

def send_emails(people):
    subject = "Natal dos queiroz: seu amigo secreto!"

    with open(email_template, 'r') as template_file:
        template = template_file.read()

    for i, person in enumerate(people[:-1]):
        body = template.format(
            name=person["name"], 
            friend=people[i+1]["name"],
            suggestion=people[i+1]["gift_suggestion"]
        )
        
        send_mail_from_template(to_email=person["email"], subject=subject, content=body)

    body = template.format(
        name=people[-1]["name"],
        friend=people[0]["name"],
        suggestion=people[0]["gift_suggestion"]
    )
    
    send_mail_from_template(to_email=people[-1]["email"], subject=subject, content=body)


def main():
    print("Iniciando processo...")
    people = get_people_list()
    shuffled_people = shuffle_people(people)
    send_emails(shuffled_people)
    print("Sorteio e envio concluídos com sucesso!")

if __name__ == '__main__':
    main()