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
alfabeto = 'abcdefghijklmnopqrstuvwxyz'

def carregarTela():
    global t, inputInicial, inputFinal

    t = time.localtime()
    tempoInicial = time.strftime("%H:%M:%S", t)
    print(tempoInicial)
    input = {'width' : 30,
             'height' : 1}

    window = tk.Tk(className="\\Bot - VKDIGITAL")
    window.configure(bg="black")
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    titleLb = tk.Label(window, text="Olá Vendedor!", bg="black", fg="white")
    titleLb.grid(column=0, columnspan=2, row=0, ipadx=0, pady=0, sticky="nsew")

    labelInicial = tk.Label(window, text="Insira o Contato Inicial:", bg="black", fg="white")
    labelInicial.grid(column=0, row=3, ipadx=10, pady=10, sticky=tk.W)

    inputInicial = tk.Entry(window, bg="white", fg="black")
    inputInicial.grid(column=1, row=3, ipadx=10, pady=10, sticky=tk.W)

    labelInicial = tk.Label(window, text="Insira o Contato Final:", bg="black", fg="white")
    labelInicial.grid(column=0, row=4, ipadx=10, pady=10, sticky=tk.W)

    inputFinal = tk.Entry(window, bg="white", fg="black")
    inputFinal.grid(column=1, row=4, ipadx=10, pady=10, sticky=tk.W)

    resultButton = tk.Button(window, text='Salvar', command=carregarContatos, width=60)
    resultButton.grid(column=0, columnspan=2, row=5, padx=10, pady=10, sticky=tk.W)

    window.mainloop()


def carregarContatos():
    print('Carregando Contatos')
    if  inputInicial.get() != "" and inputFinal.get() != "":
        print(("Contatos Originais: {0}, {1}").format(inputInicial.get(), inputFinal.get()))
        global contato_inicial
        contato_inicial = ""
        global contato_final
        contato_final = ""

        for caractere in inputInicial.get():
            if alfabeto.find(caractere) == -1:
                contato_inicial += str(caractere)
            else:
                contato_inicial += str(alfabeto.find(caractere))

        for caractere in inputFinal.get():
            if alfabeto.find(caractere) == -1:
                contato_final += str(caractere)
            else:
                contato_final += str(alfabeto.find(caractere))

        print(("Contatos Numericos: {0}, {1}").format(contato_inicial, contato_final))

        iniciaSessao()
    else:
        print("Indique o intervalo de contratos que devem ser processados!")
        raise SystemExit


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
        element = WebDriverWait(sessao, 60).until(
            EC.presence_of_element_located((By.ID, "side"))
        )
        print('QRCode Foi lido')
        global contatoTemp
        contatoTemp = contato_inicial
        while contatoTemp <= contato_final:
            acharContato(contatoTemp)
            contatoTemp = str(int(contatoTemp)+1).rjust(9, '0')
        sair()
    except TimeoutException:
        print('O QRCode não foi lido!')
    except NoSuchElementException:
        print('O robo não conseguiu achar todos os campos necessarios!')

def acharContato(contatoTemp):
    contato = alfabeto[int(contatoTemp[0])] + alfabeto[int(contatoTemp[1])] + alfabeto[int(contatoTemp[2])] + contatoTemp[3] + contatoTemp[4] + contatoTemp[5] + contatoTemp[6] + contatoTemp[7] + contatoTemp[8]
    print(('Procurando contato {0}').format(contato))
    text = sessao.find_element_by_xpath("//div[contains(@class,'_1UWac')][contains(@class, '_3hKpJ')]//div[contains(@class,'_13NKt')][contains(@class, 'copyable-text')][contains(@class,'selectable-text')]")
    text.send_keys(Keys.CONTROL, 'a')
    text.send_keys(contato)
    try:
        element = WebDriverWait(sessao, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_3GYfN"))
        )
        element = WebDriverWait(sessao, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, "YGe90"))
        )
        print('Pesquisa Concluida')
        label = (sessao.find_element_by_class_name("YGe90")).text
        print(('Label: {0}').format(label))
        if label == "CONVERSAS":
            conversa = sessao.find_element_by_class_name("_3OvU8")
            conversa.click()
            mandarMensagem()
    except TimeoutException:
        print(('Contato {0} não encontrado!').format(contatoTemp))
    except NoSuchElementException:
        print('Ocorreu um erro na pesquisa!')

def mandarMensagem():
    try:
        element = WebDriverWait(sessao, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'p3_M1')]/div/div[2]"))
        )
        print('Enviando mensagem!')
        text = sessao.find_element_by_xpath("//div[contains(@class, 'p3_M1')]/div/div[2]")
        text.send_keys("Olá, esta é uma mensagem de teste, favor desconsiderar!")
        button = sessao.find_element_by_class_name("_4sWnG")
        button.click()
        print('Mensagem enviada!')
    except NoSuchElementException:
        print('Ocorreu um erro no envio da mensagem!')


def sair():
    print('Fechando o whatsapp')
    sessao.quit()

#Chama a função inicial
carregarTela()

tempoFinal = time.strftime("%H:%M:%S", t)
print(tempoFinal)
try:
    sessao
    sessao.quit()
except NameError:
    print('Sessao inexistente')

#Note: Some variables may have been named in Brazilian portuguese,
#so var filho = child and var pai = parent