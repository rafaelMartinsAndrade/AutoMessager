import time

def acharContato(contatoTemp):
    contato = alfabeto[int(contatoTemp[0])] + alfabeto[int(contatoTemp[1])] + alfabeto[int(contatoTemp[2])] + contatoTemp[3] + contatoTemp[4] + contatoTemp[5] + contatoTemp[6] + contatoTemp[7]
    print(contato)

alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

global contato_inicial, arrContato_inicial, contato_final, arrContato_inicial
contato_inicial = ""
inicial = "JAC11747"
arrContato_inicial = []
contato_final = ""
final = "JAC11748"
arrContato_final = []

for caractere in inicial:
    if alfabeto.find(caractere) == -1:
        arrContato_inicial.append(str(caractere))
    else:
        arrContato_inicial.append(str(alfabeto.find(caractere)))

contato_inicial = "".join(arrContato_inicial)

for caractere in final:
    if alfabeto.find(caractere) == -1:
        arrContato_final.append(str(caractere)) 
    else:
        arrContato_final.append(str(alfabeto.find(caractere))) 
contato_final = "".join(arrContato_final)

print(("Contatos Numericos: {0}, {1}").format(contato_inicial, contato_final))

global contatoTemp, arrContatoTemp
contatoTemp = contato_inicial
arrContatoTemp = arrContato_inicial

while contatoTemp <= contato_final:
    # acharContato(contatoTemp)
    print(arrContatoTemp)
    print(contatoTemp)
    print(contato_final)
    print()
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
