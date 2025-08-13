from datetime import datetime
import time

class Clientes:
    def __init__(self, nome, protocolo):
        self.nome = nome
        self.protocolo = protocolo
        self.chegada = datetime.now()
        self.atendimento = None
        self.saida = None

clientes = [
    "João", "Maria", "Pedro", "Ana", "Lucas", "Mariana", "Carlos", "Fernanda",
    "Paulo", "Beatriz", "Gustavo", "Larissa", "Thiago", "Camila", "Rafael",
    "Juliana", "Mateus", "Bianca", "Rodrigo", "Patrícia", "Vinícius", "Aline",
    "André", "Natália", "Felipe", "Carolina", "Leonardo", "Sofia", "Diego", "Isabela"
]

class Caixa:
    def __init__(self):
        self.fila = []

    def atendimento(self, clientes):
        for i, cliente in enumerate(clientes):
            self.fila.append(Clientes(cliente, i+1))
            print(self.fila[i].nome, self.fila[i].protocolo, self.fila[i].chegada)
            time.sleep(2)

# programa principal
caixa = Caixa()
caixa.atendimento(clientes)
