#Imports necessários
import time
import os
from datetime import datetime

#Imports do selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

#Imports do pyautogui
from pyautogui import *
import pyautogui
import keyboard
import random
import win32api, win32con

# Imports do Tkinter
import tkinter as tk

global alfabeto
# alfabeto = 'abcdefghijklmnopqrstuvwxyz'
alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def carregarTela():
    print('Versão do Robo: 2.0 Beta')
    global t, inputInicial, inputFinal, inputMsg

    t = time.localtime()
    input = {'width' : 30,
             'height' : 1}

    window = tk.Tk(className="\\AutoMessager - VKDIGITAL")
    window.configure(bg="black")
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    titleLb = tk.Label(window, text="Olá Vendedor!", bg="black", fg="white")
    titleLb.grid(column=0, columnspan=2, row=0, ipadx=0, pady=0, sticky="nsew")

    labelInicial = tk.Label(window, text="Insira o Contato Inicial*:", bg="black", fg="white")
    labelInicial.grid(column=0, row=3, ipadx=10, pady=10, sticky=tk.W)

    inputInicial = tk.Entry(window, bg="white", fg="black")
    inputInicial.grid(column=1, row=3, ipadx=10, pady=10, sticky=tk.W)

    labelInicial = tk.Label(window, text="Insira o Contato Final*:", bg="black", fg="white")
    labelInicial.grid(column=0, row=4, ipadx=10, pady=10, sticky=tk.W)

    inputFinal = tk.Entry(window, bg="white", fg="black")
    inputFinal.grid(column=1, row=4, ipadx=10, pady=10, sticky=tk.W)

    labelMsg = tk.Label(window, text="Insira a Mensagem:", bg="black", fg="white")
    labelMsg.grid(column=0, row=5, ipadx=10, pady=10, sticky=tk.W)

    inputMsg = tk.Entry(window, bg="white", fg="black")
    inputMsg.grid(column=1, row=5, ipadx=10, pady=10, sticky=tk.W)

    resultButton = tk.Button(window, text='Processar Contatos', command=carregarContatos, width=60)
    resultButton.grid(column=0, columnspan=2, row=6, padx=10, pady=10, sticky=tk.W)

    window.mainloop()


def carregarContatos():
    tempoInicial = time.strftime("%H:%M:%S", t)
    print(('Inicio do script: {0}').format(tempoInicial))
    print('Carregando Contatos')
    if  inputInicial.get() != "" and inputFinal.get() != "":
        print(("Contatos Originais: {0}, {1}").format(inputInicial.get(), inputFinal.get()))
        global contato_inicial, arrContato_inicial, contato_final, arrContato_inicial
        contato_inicial = ""
        arrContato_inicial = []
        contato_final = ""
        arrContato_final = []

        for caractere in inputInicial.get():
            if alfabeto.find(caractere) == -1:
                arrContato_inicial.append(str(caractere))
            else:
                arrContato_inicial.append(str(alfabeto.find(caractere)))
        contato_inicial = "".join(arrContato_inicial)

        for caractere in inputFinal.get():
            if alfabeto.find(caractere) == -1:
                arrContato_final.append(str(caractere)) 
            else:
                arrContato_final.append(str(alfabeto.find(caractere))) 
        contato_final = "".join(arrContato_final)

        print(("Contatos Numericos: {0}, {1}").format(contato_inicial, contato_final))

        iniciaSessao()
    else:
        print("Indique o intervalo de contatos que devem ser processados!")


def iniciaSessao():
    #Variáveis de configuração da sessao
    driver_path = 'chromedriver'
    download_dir = "D:\\selenium"
    options = Options()
    # options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--window-size=1400,800")

    global sessao 
    #Chama a função que abre a sessão com as configurações e o driver já prédefinidos
    sessao = webdriver.Chrome(options=options, executable_path=driver_path)
    #Redireciona a sessão para a url
    sessao.get("https://web.whatsapp.com/")
    # time.sleep(1)
    verificarQRCode()

def verificarQRCode():
    print('Esperando QRCode ser Lido')
    try:
        element = WebDriverWait(sessao, 180).until(
            EC.presence_of_element_located((By.ID, "side"))
        )
        print('QRCode Foi lido')
        global contatoTemp, arrContatoTemp
        contatoTemp = contato_inicial
        arrContatoTemp = arrContato_inicial

        while contatoTemp <= contato_final:
            acharContato()
            somou = False
            contatoSoma = []
            count = 0
            for (i, numero) in enumerate(reversed(arrContatoTemp)):
                numero = int(numero)
                if not somou:
                    if(i < 5):
                        if(numero == 9):
                            numero = 0
                        else:
                            numero += 1
                            somou = True
                    else:
                        if(numero != 25):
                            numero += 1
                            somou = True
                    count += 1
                contatoSoma.append(str(numero))
            contatoTemp = ''.join(reversed(contatoSoma))
            arrContatoTemp = list(reversed(contatoSoma))
        print('Todos os contatos foram processados')
        time.sleep(2)
        sair()
    except TimeoutException:
        print('O QRCode não foi lido!')
    except NoSuchElementException:
        print('O robo não conseguiu achar o campo de pesquisa!')

def acharContato():
    contato = alfabeto[int(arrContatoTemp[0])] + alfabeto[int(arrContatoTemp[1])] + alfabeto[int(arrContatoTemp[2])] + arrContatoTemp[3] + arrContatoTemp[4] + arrContatoTemp[5] + arrContatoTemp[6] + arrContatoTemp[7]
    print(('Procurando contato {0}').format(contato))
    text = sessao.find_element_by_xpath("//div[contains(@class,'_1UWac')][contains(@class, '_3hKpJ')]//div[contains(@class,'_13NKt')][contains(@class, 'copyable-text')][contains(@class,'selectable-text')]")
    text.send_keys(Keys.CONTROL, 'a')
    text.send_keys(contato)

    try:
        element = WebDriverWait(sessao, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_3GYfN"))
        )
    except TimeoutException:
        print(('A pesquisa demorou demais, COD0.1').format(contato))
    except NoSuchElementException:
        print('O robô não conseguiu fazer a pesquisa, COD0.2')
    
    try:
        element = WebDriverWait(sessao, 1).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Contatos')]"))
        )
        print(('O contato {0} foi encontrado, COD2').format(contato))
        # Caminho para grupo
        # //*[@id="pane-side"]/div[1]/div/div/div/div/div/div[2]/div[1]/div[1]/span/span[contains(text(),'{0}')]
        # Caminho para conversa
        # //*[@id='pane-side']/div[1]/div/div/div/div/div/div[2]/div[1]/div[1]/span/span/span[contains(text(),'{0}')]
        # Caminho para contatos
        conversa = sessao.find_element_by_xpath(("//div[contains(@class,'_3vPI2')]/div/span/span/span[contains(text(),'{0}')]").format(contato))
        conversa.click()
        mandarMensagem()

    except TimeoutException:
        print(('O contato {0} não foi encontrado, COD2.1').format(contato))
    except NoSuchElementException:
        print(('A conversa do contato {0} não foi encontrada, COD2.2').format(contato))

def mandarMensagem():
    try:
        element = WebDriverWait(sessao, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'p3_M1')]/div/div[2]"))
        )
        print('O robo está enviando a mensagem')
        text = sessao.find_element_by_xpath("//div[contains(@class, 'p3_M1')]/div/div[2]")
        if inputMsg.get() != "":
            text.send_keys(inputMsg.get())
        else:
            text.send_keys("Olá, esta é uma mensagem de teste, favor desconsiderar!")
        button = sessao.find_element_by_class_name("_4sWnG")
        button.click()
        print('A mensagem foi enviada, COD3')
    except TimeoutException:
        print('O robo não conseguiu encontrar os inputs, COD3.1')
    except NoSuchElementException:
        print('Ocorreu um erro no envio da mensagem, COD3.2')


def sair():
    print('Fechando o whatsapp')
    sessao.quit()
    t = time.localtime()
    tempoFinal = time.strftime("%H:%M:%S", t)
    print(('Final do script: {0}').format(tempoFinal))

#Chama a função inicial
carregarTela()

#Note: Some variables may have been named in Brazilian portuguese,
#so var filho = child and var pai = parent