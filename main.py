from datetime import datetime

# Estrutura de dados para os clientes
clientes = {}

def registrar_compra():
    nome = input("Nome do cliente: ").strip()
    data_compra = input("Data da compra (DD/MM/AAAA): ").strip()
    objeto = input("Objeto comprado: ").strip()
    valor = float(input("Valor da compra: R$ "))

    # Converte a data
    try:
        data_formatada = datetime.strptime(data_compra, "%d/%m/%Y").date()
    except ValueError:
        print("Data inválida. Use o formato DD/MM/AAAA.")
        return

    # Cria o cliente se não existir
    if nome not in clientes:
        clientes[nome] = {
            "compras": [],
            "saldo": 0.0
        }

    # Adiciona a compra
    clientes[nome]["compras"].append({
        "data": data_formatada,
        "objeto": objeto,
        "valor": valor
    })
    clientes[nome]["saldo"] += valor

    print(f"Compra registrada para {nome} no valor de R$ {valor:.2f}.")

def quitar_valor():
    nome = input("Nome do cliente: ").strip()
    if nome not in clientes:
        print("Cliente não encontrado.")
        return

    valor = float(input("Valor a quitar: R$ "))

    if valor <= 0:
        print("Valor inválido.")
        return

    if valor > clientes[nome]["saldo"]:
        print(f"Valor excede o saldo do cliente (R$ {clientes[nome]['saldo']:.2f}).")
        return

    clientes[nome]["saldo"] -= valor
    print(f"Quitado R$ {valor:.2f} da dívida de {nome}.")

def listar_clientes():
    if not clientes:
        print("Nenhum cliente registrado.")
        return

    for nome, dados in clientes.items():
        print(f"\nCliente: {nome}")
        print(f"Saldo atual: R$ {dados['saldo']:.2f}")
        print("Compras:")
        for c in dados["compras"]:
            print(f"  - {c['data'].strftime('%d/%m/%Y')}: {c['objeto']} por R$ {c['valor']:.2f}")

def menu():
    while True:
        print("\n--- Menu ---")
        print("1. Registrar compra")
        print("2. Quitar valor")
        print("3. Listar clientes")
        print("4. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            registrar_compra()
        elif opcao == '2':
            quitar_valor()
        elif opcao == '3':
            listar_clientes()
        elif opcao == '4':
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
