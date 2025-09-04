# =============================
# Pilhas de cartas dos jogadores
# =============================

pilha1 = [
    {"nome": "Harry Potter", "atk": 10, "def": 5, "vel": 10},
    {"nome": "Hermione Granger", "atk": 3, "def": 2, "vel": 11},
    {"nome": "Ron Weasley", "atk": 7, "def": 6, "vel": 4},
    {"nome": "Alvo Dumbledore", "atk": 1, "def": 4, "vel": 9},
    {"nome": "Minerva McGonagall", "atk": 9, "def": 3, "vel": 2},
    {"nome": "Hagrid", "atk": 5, "def": 1, "vel": 7},
    {"nome": "Sirius Black", "atk": 2, "def": 5, "vel": 6},
    {"nome": "Remus Lupin", "atk": 6, "def": 2, "vel": 12},
    {"nome": "Neville Longbottom", "atk": 8, "def": 4, "vel": 3},
    {"nome": "Luna Lovegood", "atk": 4, "def": 6, "vel": 8}
]

pilha2 = [
    {"nome": "Lord Voldemort", "atk": 2, "def": 3, "vel": 9},
    {"nome": "Bellatrix Lestrange", "atk": 10, "def": 5, "vel": 6},
    {"nome": "Draco Malfoy", "atk": 1, "def": 2, "vel": 11},
    {"nome": "Severo Snape", "atk": 8, "def": 4, "vel": 1},
    {"nome": "Lucius Malfoy", "atk": 5, "def": 6, "vel": 7},
    {"nome": "Dolores Umbridge", "atk": 3, "def": 1, "vel": 12},
    {"nome": "Narcisa Malfoy", "atk": 7, "def": 2, "vel": 10},
    {"nome": "Pettigrew (Rabicho)", "atk": 6, "def": 3, "vel": 8},
    {"nome": "Fenrir Greyback", "atk": 9, "def": 5, "vel": 2},
    {"nome": "Barty Crouch Jr.", "atk": 4, "def": 6, "vel": 4}
]


class Carta:
    def __init__(self, name, Atk, Def, Spd):
        self.Name = name.strip()   
        self.Atk = int(Atk)       
        self.Def = int(Def)
        self.Spd = int(Spd)
            
    def __str__(self):
        return f"{self.Name} (Atk:{self.Atk}, Def:{self.Def}, Spd:{self.Spd})"


# =============================
# Função para criar carta a partir do texto
# =============================

def criar_carta(texto):
    partes = texto.split(",")  
    nome = partes[0]
    atk = partes[1]
    defesa = partes[2]
    spd = partes[3]
    return Carta(nome, atk, defesa, spd)


# =============================
# Inicializando as mãos
# =============================

handPlayer1 = []
handPlayer2 = []

for _ in range(5):
    handPlayer1.append(criar_carta(pilha1.pop(0)))
    handPlayer2.append(criar_carta(pilha2.pop(0)))


# =============================
# Contadores do jogo
# =============================

vitorias1 = 0
vitorias2 = 0
empates = 0


# =============================
# Função para repor carta
# =============================

def repor_carta():
    if pilha1 and len(handPlayer1) < 5:
        handPlayer1.append(criar_carta(pilha1.pop(0)))
    if pilha2 and len(handPlayer2) < 5:
        handPlayer2.append(criar_carta(pilha2.pop(0)))


# =============================
# Função de combate
# =============================

def combat():
    global vitorias1, vitorias2, empates

    if not handPlayer1 or not handPlayer2:
        return False 

    carta_player1 = handPlayer1.pop(0)
    carta_player2 = handPlayer2.pop(0)

    print("\n" + "="*40)
    print(f"Batalha: {carta_player1.Name} VS {carta_player2.Name}")
    print("-"*40)
    print(f"{carta_player1.Name} -> Atk:{carta_player1.Atk} | Def:{carta_player1.Def} | Spd:{carta_player1.Spd}")
    print(f"{carta_player2.Name} -> Atk:{carta_player2.Atk} | Def:{carta_player2.Def} | Spd:{carta_player2.Spd}")
    print("-"*40)

    vencedor = None

    if carta_player1.Spd > carta_player2.Spd:
        defesa_player2 = carta_player2.Def - carta_player1.Atk
        if defesa_player2 > 0:
            defesa_player1 = carta_player1.Def - carta_player2.Atk
            if defesa_player1 > 0:
                print("Empate! Ambos sobrevivem")
                vencedor = 0
            else:
                print(f"{carta_player1.Name} morreu! {carta_player2.Name} venceu a batalha")
                vencedor = 2
        else:
            print(f"{carta_player2.Name} morreu! {carta_player1.Name} venceu a batalha")
            vencedor = 1

    elif carta_player2.Spd > carta_player1.Spd:
        defesa_player1 = carta_player1.Def - carta_player2.Atk
        if defesa_player1 > 0:
            defesa_player2 = carta_player2.Def - carta_player1.Atk
            if defesa_player2 > 0:
                print("Empate! Ambos sobrevivem")
                vencedor = 0
            else:
                print(f"{carta_player2.Name} morreu! {carta_player1.Name} venceu a batalha")
                vencedor = 1
        else:
            print(f"{carta_player1.Name} morreu! {carta_player2.Name} venceu a batalha")
            vencedor = 2
    else:
        print("Velocidade igual! Ambos morrem")
        vencedor = 0

    if vencedor == 1:
        vitorias1 += 1
    elif vencedor == 2:
        vitorias2 += 1
    else:
        empates += 1

    print("="*40 + "\n")

    repor_carta()

    return True


# =============================
# Loop principal do jogo
# =============================

while (handPlayer1 or pilha1) and (handPlayer2 or pilha2):
    if not combat():
        break

# =============================
# Resultado final
# =============================

print("\n" + "="*40)
print(f"Vitórias Jogador 1: {vitorias1}")
print(f"Vitórias Jogador 2: {vitorias2}")
print(f"Empates: {empates}")

if vitorias1 > vitorias2:
    print("Jogador 1 venceu o jogo!")
elif vitorias2 > vitorias1:
    print("Jogador 2 venceu o jogo!")
else:
    print("O jogo terminou empatado!")
print("="*40)
