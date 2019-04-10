import requests, json
from urls import URL_DASHBOARD, URL_GAMEEVENTS, URL_USERPROFILE
import json


USARIO_PROFESSOR_ADMIN = "administrator"
SENHA_PROFESSOR_ADMIN = "eyHxTJcuRf43n5ox"


def request_post(url, data, headers):
    request = requests.post(url, data=json.dumps(data), headers=headers)
    return request.text

def get_token_admin_sgevents(clientid, apikey):
    '''
    Implementa este comando: curl -i -H "Content-Type: application/json" -X POST -d '{"clientid":"administrator","apikey":"YOURAPIKEY"}' http://localhost:5000/v1/token
    '''
    data = {"clientid": clientid, "apikey": apikey}
    headers = {'Content-type': 'application/json'}

    funcao = "token"

    url = URL_GAMEEVENTS+funcao

    response = request_post(url, data, headers)
    response = json.loads(response)
    return response["token"]

def get_token_sgevents(clientid, apikey, sessionid):
    '''
    Implementa este comando: curl -i -H "Content-Type: application/json" -X POST -d '{"clientid":"administrator","apikey":"YOURAPIKEY"}' http://localhost:5000/v1/token
    '''

    data = {"clientid": clientid, "apikey": apikey, "sessionid": sessionid}
    headers = {'Content-type': 'application/json'}

    funcao = "token"

    url = URL_GAMEEVENTS+funcao

    response = request_post(url, data, headers)
    response = json.loads(response)
    return response["token"]

def add_normal_player_sgevents(token, clientid, apikey):
    '''
    Implementa este comando: curl -i -H "X-AUTH-TOKEN: YOURTOKEN" -H "Content-Type: application/json" -X POST -d '{"clientid":"CLIENTID", "apikey":"APIKEY"}' http://localhost:5000/v1/clients
    :param clientid: human-readable name of the client 
    :param apikey: apikey (password) to authenticate the client
    :param role: optional role of the client (admin/normal). Normal clients are able to read/write 
    
    '''

    data = {"clientid": clientid, "apikey": apikey}
    headers = {'Content-type': 'application/json', 'X-AUTH-TOKEN': token}

    funcao = "clients"

    url = URL_GAMEEVENTS+funcao

    response = request_post(url, data, headers)
    response = json.loads(response)
    return response

def add_admin_player_sgevents(token, clientid, apikey):
    '''
    Implementa este comando: curl -i -H "X-AUTH-TOKEN: YOURTOKEN" -H "Content-Type: application/json" -X POST -d '{"clientid":"CLIENTID", "apikey":"APIKEY"}' http://localhost:5000/v1/clients
    :param clientid: human-readable name of the client 
    :param apikey: apikey (password) to authenticate the client
    :param role: optional role of the client (admin/normal). Normal clients are able to read/write 
    
    '''

    data = {"clientid": clientid, "apikey": apikey, "role": "admin"}
    headers = {'Content-type': 'application/json', 'X-AUTH-TOKEN': token}

    funcao = "clients"

    url = URL_GAMEEVENTS+funcao

    response = request_post(url, data, headers)
    response = json.loads(response)
    return response


def create_user_in_userprofile(user, password):
    data = {"username": user, "password":password}
    headers = {'Content-type': 'application/json'}

    funcao = "users"

    url = URL_USERPROFILE+funcao
    return request_post(url, data, headers)

def create_session_in_userprofile(user, password):
    data = {"username": user, "password":password}
    headers = {'Content-type': 'application/json'}

    funcao = "sessions"

    url = URL_USERPROFILE+funcao
    return request_post(url, data, headers)

# def get_user_in_userprofile(id_user):
#     data = {"username": user, "password":password}
#     headers = {'Content-type': 'application/json'}

#     funcao = "sessions"

#     url = URL_USERPROFILE+funcao
#     print(url)

#     return request_post(url, data, headers)



def criar_novo_jogador(usuario_jogador, senha_jogador):
    #Pega o token do professor administrador para ser usado na criação dos clientes no service sgevents
    token_professor = get_token_admin_sgevents(USARIO_PROFESSOR_ADMIN, SENHA_PROFESSOR_ADMIN)

    #Cria usuário em service userProfile para então gerar um client no sgevents
    responseUser = create_user_in_userprofile(usuario_jogador, senha_jogador)
    id_user = json.loads(responseUser)['id']
    
    #Cria sessão em service userProfile para então poder gerar uma session (pois há a verificação do uuid - ID da session) no sgevents
    responseSession = create_session_in_userprofile(usuario_jogador, senha_jogador)
    id_session = json.loads(responseSession)['id']

    #Criando um jogador (client normal para o sgevents)
    add_normal_player_sgevents(token_professor, usuario_jogador, senha_jogador)

    return {"usuario_jogador": usuario_jogador, "senha_jogador": senha_jogador, "sessionid": id_session}



def commit_event(usuario_jogador, senha_jogador, sessionid, timestamp, events):
    """
    curl -i -H "X-AUTH-TOKEN: YOURTOKEN" -H "Content-Type: application/json" -X POST -d '{"timestamp":"DATA_DO_EVENTO: 2015-11-10T20:30:00Z","events":"{DICIONARIO_DE_EVENTOS}"}' http://localhost:5000/v1/sessions/SESSIONID/events
    """
    tokenJogador  = get_token_sgevents(usuario_jogador, senha_jogador, sessionid)
    print(tokenJogador)

    data = {"timestamp": timestamp, "events": events}
    headers = {'Content-type': 'application/json', "X-AUTH-TOKEN":tokenJogador}

    funcao = "sessions/" + sessionid + "/events"

    url = URL_GAMEEVENTS+funcao

    print(url)
    return request_post(url, data, headers)

if __name__ == "__main__":
    # Simulating the input of data teacher in sgevents service and userprofile service: 
    # USARIO_PROFESSOR_ADMIN = str(input("Usuario professor: "))
    # SENHA_PROFESSOR_ADMIN = str(input("Senha professor: "))

    # Testing create one new client in service sgevents that means create one player in game:
    # jogador = criar_novo_jogador("agora vai", "12345")
    # print(jogador)

    # Testing commit the event:
    # Datas tests:
    jogador = {}
    jogador["usuario_jogador"] = "agora vai"
    jogador["senha_jogador"] = "12345"
    jogador["sessionid"] = "c642c8050171eaedc93d70ce66c6955e"

    # Testing one real commit from event:
    timestamp = "2019-04-09T20:30:00Z" 
    events = [{"id_questao": "10", "nota": "1"}]
    a = commit_event(jogador["usuario_jogador"], jogador["senha_jogador"], jogador["sessionid"],  timestamp, events)
    print(a)

