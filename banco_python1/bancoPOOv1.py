import os
import time
from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty


class Conta_iterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            self._index += 1
            return conta
        except IndexError:
            raise StopIteration


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.Registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Pessoa_Fisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self.numero = numero
        self.cliente = cliente
        self.historico = Historico()
        self.agencia =  '0001'


    @classmethod
    def Nova_conta_cliente(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property #pois é privado
    def saldo(self):
        return self._saldo

    def sacar(self, valor):
        saldo = self._saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print('transação incapaz')
            return False
        
        elif valor > 0:
            self._saldo -= valor
            print('transação feita')
            return True
        else:
            print('valor invalido')
            return False
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('deposito feito')
            return True
        else:
            print('erro deposito')
            return False

class Conta_Corrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor): # mais um pois esse eh o tipo para conta corrente
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__]
        )
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("excedeu limite")

        elif excedeu_saques:
            print('excedeu saques')
        else:
            return super().sacar(valor)
        
        return False

    def __str__(self):
        return f"""
            Agência: \t {self.agencia}
            C/C: \t {self.numero}
            Titular \t {self.cliente.nome}

        """

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self,transacao):
        self._transacoes.append(
            {
            "tipo": transacao.__class__.__name__,
            'valor': transacao.valor,
            'data' : datetime.now().strftime('%H:%M:%S - %d/%m/%Y')
            }
        )
    
    def gerar_relatorio(self, tipo_transacao = None):
        if self.historico.transacoes == []:
            yield None
        else:
            for transacao in self.historico.transacoes:
                if tipo_transacao == transacao['tipo'] or tipo_transacao == None:
                    yield transacao

class Transação(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass


    @abstractclassmethod
    def Registrar(self, conta):
        pass

class Saque(Transação):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def Registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transação):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def Registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def log_transacao(funcao):
    def envelope(*args, **kwargs):
        resultado = funcao(*args, **kwargs)
        print(f'LOG {funcao.__name__.upper()} {datetime.now()}')
        return resultado
    
    return envelope
    

def validar_cliente(cpf, clientes):
    for cliente in clientes: # conferir se o cpf existe
        if cpf == cliente.cpf:
            return cliente
    return None

def Criar_cliente(clientes):
    
    cpf = input('digite cpf: ')
    cliente = validar_cliente(cpf= cpf, clientes= clientes)

    if cliente != None:
        print('CPF ja registrado')
        return
    else:
        nome = str(input('Nome: '))
        nascimento = input('Nascimento: ')
        endereco = input('Endereco: ')
        cliente = Pessoa_Fisica(nome= nome, cpf= cpf, data_nascimento=nascimento, endereco= endereco)
        clientes.append(cliente)
        print("Cliente cadastrado, bem vindo(a)!")

@log_transacao
def Criar_conta(contas,clientes,numero_conta):
    cpf = input('Digite o seu CPF: ')
    cliente = validar_cliente(cpf= cpf, clientes= clientes)
    if cliente == None:
        print('CPF invalido')
        return
    conta = Conta_Corrente.Nova_conta_cliente(cliente= cliente, numero= numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print('Conta criada com sucesso')
    print(f'Numero da nova conta: {numero_conta}')

def validar_conta(cliente):
    conta = input('Digite o numero da sua conta: ')
    for i in cliente.contas:
        if conta == str(i.numero):
            return i
    return

@log_transacao
def depositar(clientes):
    cpf = input('Digite seu CPF: ')
    cliente = validar_cliente(cpf=cpf, clientes=clientes) # se cpf/cliente existe
    if cliente == None:
        print('Cliente não encontrado')
        return
    if cliente.contas == []: # se existe contas em seu nome
        print("Não existem contas vinculadas a este cliente")
        return
    conta = validar_conta(cliente)
    if conta == None: # conta nao existente
        print("Conta não existente")
        return

    valor = float(input("Digite o valor do deposito: "))
    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)
    print(f'Novo saldo: {conta.saldo}')

@log_transacao
def sacar(clientes):
    cpf = input('Digite seu CPF: ')
    cliente = validar_cliente(cpf=cpf, clientes=clientes) # se cpf/cliente existe
    if cliente == None:
        print('Cliente não encontrado')
        return
    if cliente.contas == []: # se existe contas em seu nome
        print("Não existem contas vinculadas a este cliente")
        return
    conta = validar_conta(cliente)
    if conta == None: # conta nao existente
        print('Conta não existente')
        return
    print(f'Saldo disponível: {conta.saldo}')
    valor = float(input("Digite o valor do saque: "))
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)
    print(f'Novo saldo: {conta.saldo}')

@log_transacao
def mostrar_historico(clientes):
    cpf = input('Digite seu CPF: ')
    cliente = validar_cliente(cpf=cpf, clientes=clientes) # se cpf/cliente existe
    if cliente == None:
        print('Cliente não encontrado')
        return
    if cliente.contas == []: # se existe contas em seu nome
        print("Esse clienten não tem contas")
        return
    conta = validar_conta(cliente)
    if conta == None: # conta nao existente
        return
    
    filtrar = input("Filtro: [d] - Deposito / [s] - Saque / [n] - Nenhum\n")
    filtro = None
    match filtrar:
        case 'd':
            filtro = 'Deposito'
        case 's':
            filtro = "Saque"
    
    print('========= Extrato =========')

    for transacao in Historico.gerar_relatorio(conta, filtro):
        if transacao == None:
            print('vazio')
            break
        print(f'\n-{transacao['tipo']}\n\tR${transacao['valor']:.2f}\n\t{transacao['data']}')
    print('===========================')


def listar_contas(contas):
    print('-' * 50)
    for i in Conta_iterador(contas):
        print(f'''
        Agência: 0001
        Titular: {i.cliente.nome}
        CPF: {i.cliente.cpf}
        C/C: {i.numero}
        Saldo: R${i.saldo:.2f}
''')    
        print('-' * 50)


def main():
    clientes = []
    contas = []
    menu = """

[c] Criar Usuario
[n] Criar conta
[d] Depositar
[s] Sacar
[e] Extrato

[q] Sair
=> """

    while True:
        
        print(menu)
        opcao = input('Opção: ')

        if opcao == 'c':
            # os.system('cls')
            Criar_cliente(clientes)
            time.sleep(1)
        elif opcao == 'n':
            # os.system('cls')
            numero_conta = len(contas) + 1
            Criar_conta(numero_conta= numero_conta, contas=contas, clientes=clientes)
            time.sleep(1)
        elif opcao == 'd':
            # os.system('cls')
            depositar(clientes)
            time.sleep(1)
        elif opcao == 's':
            # os.system('cls')
            sacar(clientes)
            time.sleep(1)

        elif opcao == 'e':
            # os.system('cls')
            mostrar_historico(clientes)
            time.sleep(1)

        elif opcao == 'l':
            listar_contas(contas)

        elif opcao == 'q':
            break
        else:
            # os.system('cls')
            print("opcao invalida")

main()