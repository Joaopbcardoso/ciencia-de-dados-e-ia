class Pilha:
    def __init__(self):
        self.itens = []

    def empilhar(self, item):
        self.itens.append(item)

    def desempilhar(self):
        if not self.esta_vazia():
            return self.itens.pop()
        return None

    def esta_vazia(self):
        return len(self.itens) == 0


def eh_palindromo(texto):
    # Normaliza: remove espaços e coloca tudo em minúsculo
    texto = ''.join(texto.split()).lower()

    pilha = Pilha()

    # Passo 1: empilhar todos os caracteres
    for letra in texto:
        pilha.empilhar(letra)

    # Passo 2: formar a string invertida desempilhando
    invertido = ''
    while not pilha.esta_vazia():
        invertido += pilha.desempilhar()

    # Passo 3: comparar
    return texto == invertido


# Exemplo de uso
palavra = input("Digite uma palavra ou frase: ")
if eh_palindromo(palavra):
    print("É um palíndromo!")
else:
    print("Não é um palíndromo.")
