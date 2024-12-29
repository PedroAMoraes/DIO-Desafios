import os

saldo = 0
saques = 0
LIMITE_DIARIO = 3
LIMITE_SAQUE = 500
acao = ''
extrato = [''] ##salvar o valor
tipo = [''] ##salvar tipo

MENU_PRINCIPAL = '''
    ---===  BANCO TESTE ===---

        [1] - Extrato
        [2] - Depositar
        [3] - Sacar
        [0] - Sair

    ---===  ##########  ===---
'''
MENU_SAIDA = '\n\n    Aperte [ENTER] para voltar'
MENU_BASE = '    ---===  ##########  ===---'

def Extrato():
    MENU_EXTRATO = '''
    ---===   Extrato   ===---

    Usuário teste

    Extrato: 
    
'''


    print(MENU_EXTRATO)
    for i in range(0,len(extrato)):
        if(extrato[i] == ''):
            break
        else:
            print(f"    {i+1}- {''.join(tipo[i])}: R${extrato[i]:.2f}")
    print(MENU_SAIDA)
    print(MENU_BASE)
    input('')

def Depositar():
    global saldo, extrato, tipo
    deposito = 0
    MENU_DEPOSITO = '\n    ---===  Depositar  ===---\n\n'

    print(MENU_DEPOSITO)
    deposito = (float(input("     Valor: R$ ")))
    saldo += deposito
    print(MENU_SAIDA)
    print(MENU_BASE)

    for i in range(0, 100):
        if i == len(extrato):
            extrato.append('') ##aumentar tamanho do array
        if (extrato[i] == ''):
            extrato[i] = deposito
            tipo.append('') 
            tipo[i] = str("Deposito") ##adicionar q o tipo foi de deposito
            break
    input()

def Saque():
    global saldo, extrato, tipo, LIMITE_DIARIO, LIMITE_SAQUE,saques
    saque = 0
    MENU_SAQUE = '\n    ---===    Sacar    ===---\n\n'

    print(MENU_SAQUE)
    saque = float(input("   Valor: R$ "))
    if(saques >= LIMITE_DIARIO):
        print("\n   Limite diário de saque atingido!")
    elif(saque > saldo):
        print("\n   Saldo insuficiente!")
    elif(saque > LIMITE_SAQUE):
        print("\n   Valor maior que o permitido diariamente!")
    else:
        saldo -= saque
        saques += 1
        for i in range(0, 100):
            if i == len(extrato):
                extrato.append('') ##aumentar tamanho do array
            if (extrato[i] == ''):
                extrato[i] = saque
                tipo.append('') 
                tipo[i] = str("Saque") ##adicionar q o tipo foi de saque
                break
    print(MENU_SAIDA)
    print(MENU_BASE)
    input()
        
while True :
    print(MENU_PRINCIPAL)
    acao = input()
    os.system('cls')
    if(acao == '1'):
        Extrato()
    elif(acao == '2'):
        Depositar()
    elif(acao == '3'):
        Saque()
    elif(acao == '0'):
        break
    else:
        print("Ação inválida")
    os.system('cls')