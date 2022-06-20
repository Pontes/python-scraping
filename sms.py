"""!
@mainpage Scraping de Rastreamento de Correios
Trabalho para P2 do curso de Engenharia de Software
@section Disciplina
Laborátorio de Programação com Interface com o Usuário
@section Professor
André Saraiva
@section Aluno
Almir de Souza Pontes Junior - Mat: 202021932
@author Pontes Junior
@version 1.0 - python 3.10 - Flask 2.1.2
@date 05/06/2022
@copyright GNU Public Licence
"""

from twilio.rest import Client

## Classe para envio de sms com a api da twilio
class sms:
    
    ## Inicialização da class sms pra autencicação da conta e do token do twilio
    def __init__(self):
        self.__account_sid = "AC6486e44691fca2d1d182533e4ad3d4c6"
        self.__auth_token = "c05d45ec7b6cff3d9bad43dd15a8a586"

    ## Função para o envio do sms
    def Mensagem(self, msg):
        client = Client(self.__account_sid,self.__auth_token)
        message = client.messages \
            .create(body=msg,from_='+18507505994',to="+5521999470170")
        return message.sid

"""
Não é possivel enviar o recebimento para outro numero com a conta trial
https://www.twilio.com/docs/api/errors/21608
porem chega para o meu telefone
x = sms()
x.Mensagem("teste")
"""
