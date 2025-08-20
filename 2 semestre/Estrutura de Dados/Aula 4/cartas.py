import random

# Pilhas iniciais de personagens
pilha1 = [
    "Harry Potter",
    "Hermione Granger",
    "Ron Weasley",
    "Alvo Dumbledore",
    "Minerva McGonagall",
    "Hagrid",
    "Sirius Black",
    "Remus Lupin",
    "Neville Longbottom",
    "Luna Lovegood"
]

pilha2 = [
    "Lord Voldemort",
    "Bellatrix Lestrange",
    "Draco Malfoy",
    "Severo Snape",
    "Lucius Malfoy",
    "Dolores Umbridge",
    "Narcisa Malfoy",
    "Pettigrew (Rabicho)",
    "Fenrir Greyback",
    "Barty Crouch Jr."
]

class Carta:
    def __init__(self, name):
        self.Name = name
        self.Atk = random.randint(1,6)
        self.Def = random.randint(3,12)
        self.Spd = random.randint(1,10)
    
    def __str__(self):
        return f"{self.Name} (Atk:{self.Atk}, Def:{self.Def}, Spd:{self.Spd})"

handPlayer1 = []
handPlayer2 = []

for i in range(5):
    handPlayer1.append(Carta(pilha1.pop(-1)))
    handPlayer2.append(Carta(pilha2.pop(-1)))

vitorias1 = 0
vitorias2 = 0
empates = 0

def combat():
    vitorias1 = 0
    vitorias2 = 0
    empates = 0
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

for i in range(5):
    combat()

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
