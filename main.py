import pickle
import os
import csv

from random import shuffle

from decouple import config

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, Content, Email

people_csv = 'people.csv'
people_filename = 'people.pkl'
email_template = 'email_template.html'

def get_people_list():
    people = []

    with open(people_csv, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            people.append(row)

    return people

def shuffle_people(people):
    #Check if it has a previus draw
    if not os.path.isfile(people_filename):
        print('New draw, shuffling people...')

        shuffle(people)

        with open(people_filename, 'wb') as picke_file:
            pickle.dump(people, picke_file)
        
        return people
    
    with open(people_filename, 'rb') as picke_file:
        return pickle.load(picke_file)

def send_message(mail):
    try:
        sg = SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
        sg.client.mail.send.post(request_body=mail.get())
    except Exception as e:
        print(e)

def send_emails(people):
    from_email = Email("nataldosqueiroz@gmail.com")
    subject = "Natal dos Queiroz: seu amigo secreto!"

    with open(email_template, 'r') as template_file:
        template = template_file.read()

    for i, person in enumerate(people[:-1]):
        body = template.format(name=person["name"], friend=people[i+1]["name"])
        content = Content("text/html", body)
        to_email = To(person["email"])
        mail = Mail(from_email, to_email, subject, content)
        send_message(mail)


    body = template.format(name=people[-1]["name"], friend=people[0]["name"])
    content = Content("text/html", body)
    to_email = To(people[-1]["email"])
    mail = Mail(from_email, to_email, subject, content)
    send_message(mail)


def main():
    print("Iniciando processo...")
    people = get_people_list()
    shuffled_people = shuffle_people(people)
    send_emails(shuffled_people)
    print("Sorteio e envio concluídos com sucesso!")

if __name__ == '__main__':
    main()