import pandas as pd
import PySimpleGUI as sg

# Full list and dataframe for the states
Fullstates = [['Acre', 'AC'],
              ['Alagoas' ,'AL'],
              ['Amapá', 'AP'],
              ['Amazonas', 'AM'],
              ['Bahia', 'BA'],
              ['Ceará', 'CE'],
              ['Distrito Federal', 'DF'],
              ['Espírito Santo', 'ES'],
              ['Goiás', 'GO'],
              ['Maranhão', 'MA'],
              ['Mato Grosso', 'MT'],
              ['Mato Grosso do Sul', 'MS'],
              ['Minas Gerais', 'MG'],
              ['Pará', 'PA'],
              ['Paraíba', 'PB'],
              ['Paraná', 'PR'],
              ['Pernambuco', 'PE'],
              ['Piauí', 'PI'],
              ['Rio de Janeiro', 'RJ'],
              ['Rio Grande do Norte', 'RN'],
              ['Rio Grande do Sul', 'RS'],
              ['Rondônia', 'RO'],
              ['Roraima', 'RR'],
              ['Santa Catarina', 'SC'],
              ['São Paulo', 'SP'],
              ['Sergipe', 'SE'],
              ['Tocantins', 'TO']]

# List of states names to be shown in the combobox
StatesAcronyms = []
for s in Fullstates:
    StatesAcronyms.append(s[1])

# List of airports
airports = [['BSB','SBBR','Aeroporto Internacional de Brasília / Presidente Jucelino Kubitschek','Brasília','DF','Brasil'],
            ['CGH','SBSP','Aeroporto Internacional de São Paulo / Congonhas','São Paulo','SP','Brasil'],
            ['GIG','SBGL','Aeroporto Internacional do Rio de Janeiro / Galeão-Antônio Carlos Jobim','Galeão','RJ','Brasil'],
            ['SSA','SBSV','Aeroporto Internacional de Salvador / Deputado Luis Eduardo Magalhães','Salvador','BA','Brasil'],
            ['FLN','SBFL','Aeroporto Internacional de Florianópolis / Hercílio Luz','Florianópolis','SC','Brasil'],
            ['POA','SBPA','Aeroporto Internacional de Porto Alegre / Salgado Filho','Porto Alegre','RS','Brasil'],
            ['VCP','SBKP','Aeroporto Internacional de Viracopos / Campinas','Campinas','SP','Brasil'],
            ['REC','SBRF','Aeroporto Internacional do Recife/ Guararapes – Gilberto Freyre','Recife','PE','Brasil'],
            ['CWB','SBCT','Aeroporto Internacional de Curitiba / Afonso Pena','Curitiba','PR','Brasil'],
            ['BEL','SBBE','Aeroporto Internacional de Belém / Val de Cans','Belém','PA','Brasil'],
            ['VIX','SBVT','Aeroporto de Vitória – Eurico de Aguiar Salles','Vitória','ES','Brasil'],
            ['SDU','SBRJ','Aerorporto Santos Dumont','Santos Dumont','RJ','Brasil'],
            ['CGB','SBCY','Aeroporto Internacional de Cuiabá / Marechal Rondon','Cuiabá','MT','Brasil'],
            ['CGR','SBCG','Aeroporto Internacional de Campo Grande','Campo Grande','MS','Brasil'],
            ['FOR','SBFZ','Aeroporto Internacional de Fortaleza / Pinto Martins','Fortaleza','CE','Brasil'],
            ['MCP','SBMQ','Aeroporto Internacional de Macapá','Macapá','AP','Brasil'],
            ['MGF','SBMG','Aeroporto Regional de Maringá / Silvio Name Junior','Maringá','PR','Brasil'],
            ['GYN','SBGO','Aeroporto de Goiânia / Santa Genoveva','Goiânia','GO','Brasil'],
            ['NVT','SBNF','Aeroporto Internacional de Navegantes / Ministro Victor Konder','Navegantes','SC','Brasil'],
            ['MAO','SBEG','Aeroporto Internacional de Manaus / Eduardo Gomes','Manaus','AM','Brasil'],
            ['NAT','SBNT','Aeroporto Internacional de Natal / Augusto Severo','Natal','RN','Brasil'],
            ['BPS','SBPS','Aeroporto Internacional de Porto Seguro','Porto Seguro','BA','Brasil'],
            ['MCZ','SBMO','Aeroporto de Maceió / Zumbi dos Palmares','Maceió','AL','Brasil'],
            ['PMW','SSPS','Aeroporto de Palmas/Brigadeiro Lysias Rodrigues','Palmas','TO','Brasil'],
            ['SLZ','SBSL','Aeroporto Internacional de São Luís / Marechal Cunha Machado','São Luis','MA','Brasil'],
            ['GRU','SBGR','Aeroporto Internacional de São Paulo/Guarulhos-Governador André Franco Motoro','Guarulhos','SP','Brasil'],
            ['LDB','SBLO','Aeroporto de Londrina / Governador José Richa','Londrina','PR','Brasil'],
            ['PVH','SBPV','Aeroporto Internacional de Porto Velho / Governador Jorge Teixeira de Oliveira','Porto Velho','RO','Brasil'],
            ['RBR','SBRB','Aeroporto Internacional de Rio Branco / Plácido de Castro','Rio Branco','AC','Brasil'],
            ['JOI','SBJV','Aeroporto de Joinville / Lauro Carneiro de Loyola','Joinville','SC','Brasil'],
            ['UDI','SBUL','Aeroporto de Uberlândia / Ten. Cel. Av. César Bombonato','Uberlândia','MG','Brasil'],
            ['CXJ','SBCX','Aeroporto Regional de Caxias do Sul / Hugo Cantergiani','Caxias do Sul','RS','Brasil'],
            ['IGU','SBFI','Aeroporto Internacional de Foz do Iguaçu','Foz do Iguaçu','PR','Brasil'],
            ['THE','SBTE','Aeroporto de Teresina – Senador Petrônio Portella','Teresina','PI','Brasil'],
            ['AJU','SBAR','Aeroporto Internacional de Aracaju / Santa Maria','Aracaju','SE','Brasil'],
            ['JPA','SBJP','Aeroporto Internacional de João Pessoa / Presidente Castro Pinto','João Pessoa','PB','Brasil'],
            ['PNZ','SBPL','Aeroporto de Petrolina / Senador Nilo Coelho','Petrolina','PE','Brasil'],
            ['CNF','SBCF','Aeroporto Internacional de Minas Gerais / Confins – Tancredo Neves','Confins','MG','Brasil'],
            ['BVB','SBBV','Aeroporto Internacional de Boa Vista / Atlas Brasil Cantanhede','Boa Vista','RR','Brasil'],
            ['CPV','SBKG','Aeroporto de Campina Grande / Presidente João Suassuna','Campina Grande','PB','Brasil'],
            ['STM','SBSN','Aeroporto de Santarém / Maestro Wilson Fonseca','Santarém','PA','Brasil'],
            ['IOS','SBIL','Aeroporto de Ilhéus/Bahia-Jorge Amado','Ilhéus','BA','Brasil'],
            ['JDO','SBJU','Aeroporto de Juazeiro do Norte – Orlando Bezerra','Juazeiro do Norte','CE','Brasil'],
            ['IMP','SBIZ','Aeroporto de Imperatriz – Prefeito Renato Moreira','Imperatriz','MA','Brasil'],
            ['XAP','SBCH','Aeroporto de Chapecó – Serafin Enoss Bertaso','Chapecó','SC','Brasil'],
            ['MAB','SBMA','Aeroporto de Marabá','Marabá','PA','Brasil'],
            ['CZS','SBCZ','Aeroporto Internacional de Cruzeiro do Sul','Cruzeiro do Sul','AC','Brasil'],
            ['PPB','SBDN','Aeroporto Estadual de Presidente Prudente','Presidente Prudente','SP','Brasil'],
            ['CFB','SBCB','Aeroporto Internacional de Cabo Frio','Cabo Frio','RJ','Brasil'],
            ['FEN','SBFN','Aeroporto de Fernando de Noronha','Fernando de Noronha','PE','Brasil'],
            ['JTC','SJTC','Aeroporto Estadual de Bauru/Arealva','Bauru','SP','Brasil'],
            ['MOC','SBMK','Aeroporto de Montes Claros/Mário Ribeiro','Montes Claros','MG','Brasil']]
for register in airports: #concatenation of IATA and Name
    register.append(register[0] + ' - ' + register[2])

# Window for state selection
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

FilteredAirportsList = []
for row in airports:
    if row[4] == SelectedState:
        FilteredAirportsList.append(row[2])

# Window to choose the airport in the list
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
for item in airports:
    if SelectedAirport == item[2]:
        Selectediata = item[0]

print(SelectedState)
print(SelectedAirport)
print(SelectedDirection)

