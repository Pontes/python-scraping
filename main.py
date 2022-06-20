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

from calendar import timegm
from urllib.parse import _DefragResultBase
from flask import Flask, render_template, url_for, request, redirect, flash
import scraping
import db_sqlite3
import sms
import schedule
import time
import threading

## Função para verificar a mudança de Status do Objeto de Rastreado
#  A função faz a verificação em horário determinados,
#  Havendo alteração no status do Objeto e enviado um sms para o telefone cadastrado no banco
def verificarStatus():
    codigos = db_sqlite3.select_rastreio()
    for i in codigos:
        retorno = scraping.consultaCorreios(i[0])
        if i[2] != retorno[0]:
            msgRastreio = i[0] + "-" + retorno[0]
            x = sms.sms()
            x.Mensagem(msgRastreio)

## Função que execução  a verificação do objeto nos correios, a tarefa está agenda para todos os dia em um horário determinado
# No horário determinado e executada a função que verifica o status do objeto no correio.
def verificarCorreios():
    #schedule.every(10).seconds.do(verificarStatus)
    schedule.every().day.at("09:15").do(verificarStatus)
    schedule.every().day.at("18:00").do(verificarStatus)
    while True:
        schedule.run_pending()
        time.sleep(1)

## Função que irá executar threads simultaneamentes do flask e do agendamento das tarefas
def cron(jb):
    th1 = threading.Thread(target=jb)
    th1.start()
   

app = Flask(__name__)

## Rota principal do flask. Ao iniciar chamas os a função que monta as tabelas no banco sqlite caso não existam e
# Redireciona para o arquivo index.html
@app.route('/')
def index():
    db_sqlite3.monta_tabelas()
    return render_template("index.html")

## Rota que faz a verificação do status do objeto no correios, recupera os dados vindo do formulário da página index.html
@app.route('/status', methods=['POST'])
def status():

    # Verifica se os dados foram enviados via metodos POST e recupera os dados do formulário   
    if request.method == "POST":
        codigo = request.form.get('codigo_rastreio')
        envio = request.form.get('sms1')
        telefone = request.form.get('telefone')

    ## Chama a função consultaCorreios no arquivo scraping.py
    # @param codigo - código de rastreamento
    consulta =scraping.consultaCorreios(codigo)
    statusObj = str(consulta[0])

    ## Condicional que verifica se foi permitido o envio do status do objeto via sms
    if envio == "1":
        ## Chama a função  select_codigo_rastreio no arquivo db_sqlite3.py
        # @param codigo  codigo que do objeto a ser rastreado
        busca = db_sqlite3.select_codigo_rastreio(codigo)

        ## Condicional que verifica se a função select_codigo_rastreio retonar algum dado
        if busca:
            ## condicional que verifica se o resultado do select_codigo_rastreio é igual ao dados enviado pelo formulário
            # Redireciona o a página status.html o resultado da busca
            if busca[0] == codigo:
                r = "O código já está registrado!"
                return render_template('status.html', code=codigo, consulta=consulta, tam=len(consulta),resultado = r)
        else:
            ## Chama função insere_rastreio no arquivo db_sqlite3.py, que insere os dados do formulário no banco de dados
            ## Após a inserção no bando é enviado um sms para o telefone registrado.
            db_sqlite3.insere_rastreio(codigo,telefone,statusObj)
            msgRastreio = codigo + "-" + statusObj
            x = sms.sms()
            x.Mensagem(msgRastreio)
            #sms.sms.Mensagem(statusObj)
    
    ## retorno dos dados para a página status.html
    return render_template('status.html', code=codigo, consulta=consulta, tam=len(consulta))

## Rota que verifica os códigos salvos no banco de dados
@app.route('/codigossalvos')
def codigosalvo():

    ## Chama a Função select_rastreio que retorna os dados registrado no banco dos codigos, telefone e status do objeto
    ret = db_sqlite3.select_rastreio()

    ## retorno dos dados do banco para a página codigossalvos.html
    return render_template('codigossalvos.html', listar=ret)

## Rota que permite visualizar o status de um objeto da lista da página de codigos salvos
@app.route("/visualizar/<string:codigo>", methods=['GET'])
def visualizar(codigo):
    code = str(codigo)
    
    ## Chama a função consultaCorreios do arquivo scraping.py
    # @param code codigo do objeto que será pesquisado
    consulta =scraping.consultaCorreios(code)

    ## retorno do dados para a página status.html
    return render_template('status.html', consulta=consulta, tam=len(consulta))

## Rota para excluir um dado do objeto cadastrado no banco de dados
@app.route('/excluir',methods=['POST'])
def excluir():
    
    # Verifica se os dados foram enviados via metodos POST e recupera os dados do formulário do tipo hidden
    if request.method == "POST":
        deletar = request.form.get('del-codigo')
        ## Chama função remove_rastreio do arquivo scraping.py
        # @param deletar variavel que contem o codigo do objeto de rastreio
        db_sqlite3.remove_rastreio(deletar)

    ## retorno para a página de codigos salvos
    return redirect("/codigossalvos")
    
## Função que tratar rota inexistente, retornando Erro 404 página não encontrada    
@app.errorhandler(404)
def page_not_found(e): 
    return render_template('404.html'), 404
    

## função principal que executa o programa e as threads simultaneamente
if __name__ =='__main__':
    cron(app.run)
    cron(verificarCorreios)

