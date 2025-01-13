import os
import time


menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[c] Criar Usuario
[n] Criar conta
[l] Login/Trocar conta
[q] Sair

=> """

saldo = [0] ##
limite = 500
extrato = [''] ##
numero_saques = [0] ##
LIMITE_SAQUES = 3

clientes = []
contas = []
AGENCIA = '0001'
numero_contas = 0
conta_atual = 0


def Deposito( saldo, valor, extrato, conta, /):
    if valor > 0:
        saldo[conta] += valor
        extrato[conta] += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito conluído!")
        return saldo[conta], extrato[conta]
    else:
        print("Operação falhou! O valor informado é inválido.")
        return saldo[conta], extrato[conta]

def Saque(*, saldo, Limite, limite_saques, extrato, valor, numero_saques, conta):
    excedeu_saldo = valor > saldo[conta]
    excedeu_limite = valor > Limite
    excedeu_saques = numero_saques[conta] >= LIMITE_SAQUES
    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo[conta] -= valor
        extrato[conta] += f"Saque: R$ {valor:.2f}\n"
        numero_saques[conta] += 1
        print("Saque concluído!")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo[conta], extrato[conta], numero_saques[conta]

def Extrato(saldo, /, *, extrato, conta):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato[conta] else extrato[conta])
        print(f"\nSaldo: R$ {saldo[conta]:.2f}")
        print("==========================================")

def CriarUsuario(clientes):
    input("Digite seu nome: ")
    input("Digite seu nascimento: ")
    while True:
        cpf_novo = str(input("Digite seu CPF: "))
        if cpf_novo not in clientes:
            break
        else:
            print("Cpf inválido!")
    input("Digite seu endereço: ")
    return cpf_novo

def CriarConta(clientes,/, Agencia, numero_contas):
    if clientes == []:
        return 'erro'
    else:
        while True:
            cpf = input("Digite seu CPF")
            if cpf not in clientes:
                print("Cpf inválido!")
            else:
                break
            
        conta_nova = (Agencia + ' ' + str(numero_contas) + ' ' + cpf)
        
        return conta_nova

def Login():
    conta_encontrada = False
    cpf = input("Digite seu cpf: ")
    conta = input("Digite o numero de sua conta: ")
    for i in range(0, len(contas)):
        if (cpf in contas[i] and conta in contas[i]):
            print("Conta encontrada e ativa!")
            conta_encontrada = True
            break
    if conta_encontrada == False:
        print("Conta inválida! Verifique as credenciais")
        return 0
    else:
        return int(conta)

def main():
    while True:
        opcao = input(menu)

        if opcao == "d":
            os.system('cls')
            valor = float(input("Informe o valor do depósito: "))
            saldo[conta_atual], extrato[conta_atual] = Deposito(saldo, valor, extrato, conta_atual)
            time.sleep(2)
            

        elif opcao == "s":
            os.system('cls')
            valor = float(input("Informe o valor do saque: "))
            saldo[conta_atual], extrato[conta_atual], numero_saques[conta_atual]  = Saque(conta = conta_atual, valor = valor, saldo = saldo, Limite = limite, limite_saques= LIMITE_SAQUES, extrato= extrato, numero_saques= numero_saques)
            time.sleep(2)
            
        elif opcao == "e":
            os.system('cls')
            Extrato(saldo, extrato = extrato, conta = conta_atual)
            time.sleep(2)
            

        elif opcao == 'c':
            os.system('cls')
            clientes.append(CriarUsuario(clientes))
            print("Usuário cadastrado!")
            time.sleep(2)
            
        
        elif opcao == 'n':
            os.system('cls')
            numero_contas += 1
            nova_conta = CriarConta(clientes, Agencia= AGENCIA, numero_contas= numero_contas)
            if nova_conta != 'erro':
                contas.append(nova_conta)
                saldo.append(0)
                extrato.append('')
                numero_saques.append(0)
                print("Conta criada!")
            time.sleep(2)
            
        elif opcao == 'l':
            os.system('cls')
            conta_atual = Login()
            print("Você está logado!")
            time.sleep(2)
        
        elif opcao == 'o':
            os.system('cls')
            conta_atual = 0
            print("Deslogado!")
            time.sleep(2)
        elif opcao == "q":
            break
            

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")



main()