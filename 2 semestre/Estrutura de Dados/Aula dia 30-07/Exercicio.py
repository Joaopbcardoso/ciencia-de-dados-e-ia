#Realizar o cálculo da média, a maior e a menor nota de uma lista de notas

notas = [10.0, 8.5, 9.0, 7.5, 6.0, 10.0, 8.0, 9.5, 4.0, 5.5, 3.0, 2.5, 1.0, 2.0, 10.0, 9.0, 8.5, 7.0, 6.5, 5.0]

media = sum(notas) / len(notas)
print(f"A média das notas é: {media:.2f}")

def calcular_maior_nota(notas):
    maior_nota = notas[0]
    for nota in notas:
        if nota > maior_nota:
            maior_nota = nota
    print(maior_nota)

def calcular_menor_nota(notas):
    menor_nota = notas[0]
    for nota in notas:
        if nota < menor_nota:
            menor_nota = nota
    print(menor_nota)

calcular_maior_nota(notas)
calcular_menor_nota(notas)