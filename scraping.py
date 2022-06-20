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

##
# Tem por finalidade  fazer a conexão e retornar os dados do rastreio dos correios
# Nesse arquivo tem importado as bibliotecas request, beautifilsoup, constants e beautifultable

import requests # biblioteca que traz funcionalidades do protocolo http
from bs4 import BeautifulSoup # biblioteca para extrair dados de arquivos HTML e XML
from beautifultable import BeautifulTable #biblioteca que permite imprimir dados em forma de tabelas para o terminal

def urlPrincipal():
    """! @Função urlPrincipal """
    ##
    # Função urlPrincipal, contém somente a url que faz a conexão para o rastreio dos correios
    # apenas retorna a url

    return 'https://www.linkcorreios.com.br/?id='


## Função consultaCorreios
# Função consultaCorreios, uma função que recebe o código de rastreio, faz a conexão com a url e trata os dados
# recebido e retorna as informações em dados tabulares
# :param codigo: código de rastreio que é um string passada via terminal pelo usuário
# :return: retorna vazio, pois os dados já são impressos pela função
def consultaCorreios(codigo):

    ## pega os dados do request,e codifica para utf-8
    # Variavel que recebe a url e o código de rastreio e faz a conexão
    dadosCorreios = requests.get(urlPrincipal() + codigo) 
    dadosCorreios.encoding = 'utf-8'

    ## Chama a função BeautifulSoup para o tratamento dos dados do site
    #Dados recebidos da conexão tratados pela lib BeautifulSoap e convertidos em texto
    htmlCorreios = BeautifulSoup(dadosCorreios.text, 'html.parser') 
      
    # Início do tratamento e busca dos dados em uma parte específica do site na qual foi passada a url
    showCorreios = htmlCorreios.find('div', attrs={'class':'singlepost'})
    statusObjeto = showCorreios.find_all('li')
    
    l = []
    for x in statusObjeto:   
        l.append(x.text)
    
    ## Retorno em lista das informações obtidas no scraping
    return l



