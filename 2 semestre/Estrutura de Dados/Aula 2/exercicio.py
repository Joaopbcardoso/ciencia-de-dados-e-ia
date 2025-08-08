# Exercício de registro de livros usando dataclass
# Crie uma classe chamada Livro que tenha os atributos título, autor, ano de publicação e preço.
# Registrar livros e exibir suas informações.
# Desafio I: criar uma função "recente()" (<5anos)
# Desafio II: criar uma função "caro(>Média)"

from dataclasses import dataclass

@dataclass
class Livro:
    titulo: str
    autor: str
    ano: int
    preco: float

Livros = [
    Livro("O Homem Mais Inteligente da História", "Augusto Cury", 2016, 39.90),
    Livro("As Crônicas de Nárnia", "C.S. Lewis", 1950, 29.90),
    Livro("As Aventuras de Sherlock Holmes", "Arthur Conan Doyle", 1892, 19.90),
    Livro("O Deus que destroi sonhos", "Rodrigo Bibo", 2021, 49.90),
    Livro("Código Limpo", "Robert C. Martin", 2008, 89.90)
]


def recente(livros):
    livros_recentes = []
    print('Livros publicados a partir de 2020:')
    for i in livros:
        if i.ano >= 2015:
            livros_recentes.append(i.titulo)
    for livro in livros_recentes:
        print(f'- {livro}')

recente(Livros)
