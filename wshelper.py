import ssl
import os
import sys
import json
from websocket import create_connection


#PARTE 1 - VERIFICACAO DE ORIGIN
origin = False
print "WEBSOCKETS HELPER"
print "Digite o ip:porta da aplicacao a ser testada"
ws_addr = raw_input("ex. ws://192.168.25.27:8080 ou wss\n")
print "Entre o JSON de conexao inicial com a aplicacao"
ws_json = raw_input('ex. {"event":"login","data":{"player_name":"breno"}}\n')
if ws_addr.find("wss")==-1:
	ws = create_connection(ws_addr, origin="http://www.google.com")
	ws.send(ws_json)
	result =  ws.recv()
	print "Received '%s'" % result
	ws.close()
	#de acordo com a especificacao (rfc) do websocket, precisa responder 403 caso o origin seja checado.
	if len(result) > 5:
		print "Origin nao verificado"
		origin=False
	else:
		origin=True
    print "Origin seguro"

#PARTE 2 - VERIFICACAOO DE SSL
if (ws_addr.find("wss")!=-1):
	print "Por favor aguarde enquanto o testssl roda... será criado um arquivo output.html com o resultado do teste"
	os.system("./testssl/testssl.sh " + ws_addr[6:]+" | aha > output.html")
else:
	print "Endereco ws -> sem conexao segura"

#PARTE 3 - fuzzing
print "Digite o JSON para que se aplique o fuzzing"
fuzz = raw_input("")
jfuzz = json.loads(str(fuzz))
#jfuzz = json.loads('{"event":"lobby_chat","data":{"msg":"mensagem"}}')
print "Escolha qual dos parametros sera utilizado como payload"
z=0
for i in jfuzz.keys():
	print "["+str(z)+"] " + str(i)
	z=z+1
indexfuzz = int(raw_input(""))
f = open("./payloadsxss.txt")
linhas = f.readlines()
f.close()
for linha in linhas:
	print "linha: " + linha
	jfuzz[jfuzz.keys()[indexfuzz]]["msg"] = linha
	ws = create_connection(ws_addr,sslopt={'cert_reqs': ssl.CERT_NONE})
	ws.send(json.dumps(jfuzz))
	result =  ws.recv()
	print result
	ws.close()