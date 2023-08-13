# This program is for aviation lovers to know when their favorite aircrafts will be around

from datetime import datetime, timedelta
import pytz
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import PySimpleGUI as sg
import AuxiliarLists as al # File kept apart that holds auxiliary lists

# From full list of States and Acronyms, creates a new list of acronyms
StatesAcronyms = []
for s in al.Fullstates:
    StatesAcronyms.append(s[1])

# From full List of Airports
for register in al.Airports: #concatenation of IATA and Name
    register.append(register[0] + ' - ' + register[2])

# Window #1 for state selection
layout = [
    [sg.Text('Em qual estado veremos aviões hoje?')],
    [sg.Combo(StatesAcronyms, key='-COMBO-',size=(50,1))],
    [sg.Button('Ok')]]
window = sg.Window('Divirta-se com ForSpotter', layout, size=(450,100))
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Ok':
        SelectedState = values['-COMBO-']
        window.close()

# List created with airports which State equals to one selected on the previous window
FilteredAirportsList = []
for row in al.Airports: # Returns the aiports according to its state
    if row[4] == SelectedState:
        FilteredAirportsList.append(row[2])

# Window #2 to choose the airport in the list
layout = [
    [sg.Text('Qual o aeroporto mais perto de você?')],
    [sg.Combo(FilteredAirportsList, key='-COMBO-', size=(50,1))],
    [sg.Text('E qual a direção dos vôos?')],
    [sg.Radio('Decolando', 'opcoes', default=True, key='-OPCAO1-'),
     sg.Radio('Pousando', 'opcoes', key='-OPCAO2-')],
    [sg.Button('Ok')]]

window = sg.Window('Divirta-se com ForSpotter', layout)
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Ok' and values['-OPCAO1-']:
        SelectedAirport = values['-COMBO-']
        SelectedDirection = 'Departure'
    elif event == 'Ok' and values['-OPCAO2-']:
        SelectedAirport = values['-COMBO-']
        SelectedDirection = 'Arrival'
    window.close()

# According to the airport name, it returns the iata code that will feed the API URL
for item in al.Airports:
    if SelectedAirport == item[2]:
        SelectedIata = item[0]

# Research limited to the next hour, so returns revised time (more accurate than scheduled)

# Time Zone adjustment
timezone_br = pytz.timezone('America/Sao_Paulo')

# initial and final date
initial = datetime.now(timezone_br).strftime("%Y-%m-%dT%H:%M")
final = (datetime.now(timezone_br) + timedelta(hours = 1)).strftime("%Y-%m-%dT%H:%M")

# API connection (create and API Key on RapidAPI
url = f"https://aerodatabox.p.rapidapi.com/flights/airports/IATA/{SelectedIata}/{initial}/{final}"

headers = {
    "X-RapidAPI-Key": "CREATE YOUR OWN API KEY",
    "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
}

dados = requests.get(url, headers=headers)
result = dados.json()

RelevantFlights = [] # Next non cancelled flights AND with aircraft information, heading to the desired direction
NextAircrafts = [] # List of every aircraft that will pass by within next period

# Boolean list for direction selection on screen
if SelectedDirection == 'Departure':
    direction = 'departures'
elif SelectedDirection == 'Arrival':
    direction = 'arrivals'

# Checks if aircraft info is available, that flight is not cancelled and appends the flight to the list
for item in result[direction]:
     if 'aircraft' in item.keys():
        RelevantFlights.append(item)
        NextAircrafts.append(item['aircraft']['model'])

# Cria lista única de proximas aeronaves
UniqueNextAicrafts = sorted(set(NextAircrafts))

# Window #3 To select which aircraft models are interesting for the user
layout = [[sg.Text('Essas aeronaves passarão em breve')],
          [sg.Text('Escolha as que gosta mais')],
          [sg.Listbox(values=UniqueNextAicrafts, size=(30, 6), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, key='-LIST-')],
          [sg.Button('OK'), sg.Button('Cancelar')]]

window = sg.Window('Divirta-se com ForSpotter', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Cancelar':
        break
    elif event == 'OK':
        SelectedAircrafts = values['-LIST-']
        break

window.close()

# List with relevant flights to be emailed
FlightsTable = {'Voo': [], 'Aeronave':[], 'Cia':[], 'Status': [], 'Horario Previsto':[], 'Horario Ajustado':[]}

# In every relevant flight, checks if the aircraft model is in the selected list and appends it to the table in html
for flight in RelevantFlights:
    if flight['aircraft']['model'] in SelectedAircrafts:
            FlightDate = datetime.strptime(flight['movement']['scheduledTime']['local'], "%Y-%m-%d %H:%M%z")
            FlightTime = FlightDate.strftime("%H:%M")
            RevisedDate = datetime.strptime(flight['movement']['revisedTime']['local'], "%Y-%m-%d %H:%M%z")
            RevisedTime = RevisedDate.strftime("%H:%M")
            FlightsTable['Voo'].append(flight['number'])
            FlightsTable['Horario Previsto'].append(FlightTime)
            FlightsTable['Horario Ajustado'].append(RevisedTime)
            FlightsTable['Aeronave'].append(flight['aircraft']['model'])
            FlightsTable['Cia'].append(flight['airline']['name'])
            FlightsTable['Status'].append(flight['status'])
FinalTable = pd.DataFrame(FlightsTable)

# Criar a interface gráfica com o campo de entrada de texto
layout = [[sg.Text('Onde quer receber a tabela?')],
          [sg.Input(key='-INPUT-')],
          [sg.Button('OK'), sg.Button('Cancelar')]]

window = sg.Window('Divirta-se com ForSpotter', layout)
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Cancelar':
        break
    elif event == 'OK':
        SelectedEmail = values['-INPUT-']
        break

window.close()

FinalTable_html = FinalTable.to_html(index=False)

# Email - Outlook SMTP settings
smtp_server = 'smtp-mail.outlook.com'
smtp_port = 587
sender_email = 'INSERT AN OUTLOOK EMAIL TO BE USED AS SENDER'
password = 'INSERT THE PASSWORD OF THE EMAIL WRITTEN ABOVE'

# Criar mensagem
message = MIMEMultipart("alternative")
message['From'] = sender_email
message['To'] = SelectedEmail
message['Subject'] = f'Vôos para admirar =)'

html_part = MIMEText(FinalTable_html,"html")

message.attach(html_part)

# Conectar ao servidor SMTP do Outlook.com
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(sender_email, password)

# Enviar e-mail
server.sendmail(sender_email, SelectedEmail, message.as_string())
server.quit()

