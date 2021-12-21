# server.py
import socket
import json
import threading

def processingDataClient(received):
    # IMC (Indice de Massa Corporal)
    def generateImc(dict):
        h = dict['altura']
        p = dict['peso']
        return round(float(p / (h * h)), 2)

    # adding the imc to data sent by the user
    received['imc'] = generateImc(received)

    # Status IMC
    def analyseImc(imc):
        if imc > 0 and imc < 18.5:
            status = "Abaixo do Peso!"
        elif imc <= 24.9:
            status = "Peso normal!"
        elif imc <= 29.9:
            status = "Sobrepeso!"
        elif imc <= 34.9:
            status = "Obesidade Grau 1!"
        elif imc <= 39.9:
            status = "Obesidade Grau 2!"
        elif imc <= 40.0:
            status = "Obesidade Grau 1!"
        else:
            status = "Valores inválidos"
        return status

    # adding the status of the imc to data sent by the user
    received['statusImc'] = analyseImc(received['imc'])

    # TMB (Taxa Metabólica Basal)
    def generateTMB(dict):
        sex = dict['sexo']

        if sex in 'Mm':
            tmb = 5 + (10 * dict['peso']) + (6.25 * (dict['altura'] * 100)) - (5 * dict['idade'])

        else:
            tmb = (10 * dict['peso']) + (6.25 * (dict['altura'] * 100)) - (5 * dict['idade']) - 5

        return tmb

    # adding the tmb to data sent by the user
    received['tmb'] = generateTMB(received)

    def generateCal(dict):
        if dict['nvlAtiv'] == 1:
            fatorAtiv = 1.2

        elif dict['nvlAtiv'] == 2:
            fatorAtiv = 1.375

        elif dict['nvlAtiv'] == 3:
            fatorAtiv = 1.725

        else:
            fatorAtiv = 1.9

        return round((dict['tmb'] * fatorAtiv), 2)

    # adding the cal to data sent by the user
    received['cal'] = generateCal(received)

    def generateNutrients(dict):
        carb = str(round((dict['cal'] * 0.45), 2))
        prot = str(round((dict['cal'] * 0.3), 2))
        fat = str(round((dict['cal'] * 0.25), 2))

        return {"carboidratos": carb, "proteinas": prot, "gorduras": fat}

    # adding the nutrients to data sent by the user
    received["nutrientes"] = generateNutrients(received)
    return received

def handleClient(clientSocket, addr):
    print('Conectado a {}'.format(str(addr)))

    # recive client data
    received = clientSocket.recv(1024).decode()
    print('Os dados recebidos do cliente são: {}'.format(received))

    # server processing
    received = json.loads(received)
    data = processingDataClient(received)
    print('O resultado do processamento é {}'.format(data))

    # serialising
    result = json.dumps(data)

    # send a result
    clientSocket.send(result.encode('ascii'))
    print('Os dados do cliente: {} foram enviados com sucesso!'.format(addr))

    # finish a connection
    clientSocket.close()

# create a socket object
print('ECHO SERVER para cálculo do IMC')
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get a local machine name
host = '127.0.0.1'
port = 9999

# bind to the port
serverSocket.bind((host, port))

#start listening requests
serverSocket.listen()
print('Serviço rodando na porta {}.'.format(port))

while True:
    # establish a connection
    clientSocket, addr = serverSocket.accept()
    t = threading.Thread(target=handleClient, args=(clientSocket, addr))
    t.start()