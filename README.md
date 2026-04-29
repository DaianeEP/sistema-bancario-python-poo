# 🏦 Sistema Bancário em Python com POO

Este projeto é uma implementação de um sistema bancário moderno, focado em **Programação Orientada a Objetos (POO)**. Ele foi desenvolvido seguindo um modelo de classes UML para garantir organização e escalabilidade.

## 🚀 Funcionalidades

- **Gestão de Clientes:** Cadastro de pessoas físicas com endereço e dados pessoais.
- **Contas Múltiplas:** Um cliente pode possuir uma ou mais contas bancárias.
- **Operações Financeiras:** Depósitos e saques validados por regras de negócio.
- **Limite de Saques:** Controle diário de quantidade e valor máximo por transação.
- **Extrato Detalhado:** Histórico completo com data e hora de cada movimentação.

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Módulos:** `datetime`, `abc` (Abstract Base Classes), `textwrap`.

## 📋 Modelo de Classes (UML)
O sistema foi estruturado com base nos seguintes conceitos de POO:
- **Herança:** `PessoaFisica` herda de `Cliente` e `ContaCorrente` de `Conta`.
- **Interfaces/Abstração:** Uso de classes abstratas para definir o contrato de `Transação`.
- **Composição:** A `Conta` possui um `Historico` que contém várias `Transações`.

## 📦 Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com
   ```
2. Navegue até a pasta:
   ```bash
   cd seu-repositorio
   ```
3. Execute o sistema:
   ```bash
   python sistema_bancario.py
   ```
