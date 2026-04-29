from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

# ============================================================
# CLASSES DE MODELO (SEGUINDO O DIAGRAMA UML)
# ============================================================

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self): pass

    @property
    @abstractmethod
    def data(self): pass

    @abstractmethod
    def registrar(self, conta): pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.now()

    @property
    def valor(self): return self._valor

    @property
    def data(self): return self._data

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.now()

    @property
    def valor(self): return self._valor

    @property
    def data(self): return self._data

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    @property
    def saldo(self): return self._saldo
    @property
    def numero(self): return self._numero
    @property
    def agencia(self): return self._agencia
    @property
    def cliente(self): return self._cliente
    @property
    def historico(self): return self._historico

    def sacar(self, valor):
        if valor > self._saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
            return False
        if valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        print("\n@@@ Operação falhou! Valor inválido. @@@")
        return False

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500.0, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        hoje = datetime.now().date()
        saques_hoje = [t for t in self.historico.transacoes if isinstance(t, Saque) and t.data.date() == hoje]
        
        if valor > self.limite:
            print("\n@@@ Falha: O valor excede o limite por saque. @@@")
            return False
        if len(saques_hoje) >= self.limite_saques:
            print("\n@@@ Falha: Limite diário de saques atingido. @@@")
            return False
        return super().sacar(valor)

    def __str__(self):
        return f"Agência:\t{self.agencia}\nC/C:\t\t{self.numero}\nTitular:\t{self.cliente.nome}"

# ============================================================
# FUNÇÕES DE MENU E INTERAÇÃO
# ============================================================

def filtrar_cliente(cpf, clientes):
    filtrados = [c for c in clientes if c.cpf == cpf]
    return filtrados[0] if filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    valor = float(input("Valor do depósito: "))
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, Deposito(valor))

def sacar(clientes):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    valor = float(input("Valor do saque: "))
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, Saque(valor))

def exibir_extrato(clientes):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente: return
    conta = recuperar_conta_cliente(cliente)
    if not conta: return

    print("\n================ EXTRATO ================")
    if not conta.historico.transacoes:
        print("Sem movimentações.")
    else:
        for t in conta.historico.transacoes:
            print(f"[{t.data.strftime('%d/%m/%Y %H:%M')}] {t.__class__.__name__}: R$ {t.valor:.2f}")
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("==========================================")

def main():
    clientes, contas = [], []
    while True:
        opcao = input("\n[d] Depósito [s] Saque [e] Extrato [nc] Nova Conta [nu] Novo User [q] Sair\n=> ")
        if opcao == "d": depositar(clientes)
        elif opcao == "s": sacar(clientes)
        elif opcao == "e": exibir_extrato(clientes)
        elif opcao == "nu":
            cpf = input("CPF: ")
            if filtrar_cliente(cpf, clientes): print("CPF já cadastrado!"); continue
            clientes.append(PessoaFisica(cpf, input("Nome: "), input("Data (dd-mm-aaaa): "), input("Endereço: ")))
        elif opcao == "nc":
            cpf = input("CPF: ")
            cliente = filtrar_cliente(cpf, clientes)
            if cliente:
                conta = ContaCorrente.nova_conta(cliente, len(contas) + 1)
                contas.append(conta); cliente.adicionar_conta(conta)
                print("\n=== Conta criada! ===")
        elif opcao == "q": break

if __name__ == "__main__":
    main()
