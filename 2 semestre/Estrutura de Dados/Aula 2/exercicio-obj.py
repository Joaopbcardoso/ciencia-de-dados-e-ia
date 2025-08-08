class Livro:
    def __init__(self, titulo, autor, ano, preco):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.preco = preco

Livros = [
    Livro("O Homem Mais Inteligente da História", "Augusto Cury", 2016, 39.90),
    Livro("As Crônicas de Nárnia", "C.S. Lewis", 1950, 29.90),
    Livro("As Aventuras de Sherlock Holmes", "Arthur Conan Doyle", 1892, 19.90),
    Livro("O Deus que destroi sonhos", "Rodrigo Bibo", 2021, 49.90),
    Livro("Código Limpo", "Robert C. Martin", 2008, 89.90)
]

def buscar_livro(titulo, livros):
    for livro in livros:
        if livro.titulo.lower() == titulo.lower():
            return livro
    return False

def atual(livro):
    if livro.ano >= 2015:
        return f'foi publicado a partir de 2015.'
    else:
        return f'foi publicado antes de 2015.'

def caro(livro, livros):
    media = sum(l.preco for l in livros) / len(livros)
    if livro.preco > media:
        return f'é caro, pois custa mais que a média de R${media:.2f}.'
    else:
        return f'não é caro, pois custa menos que a média de R${media:.2f}.'

# Programa principal
livro_procurado = input("Digite o título do livro (ou 'sair' para encerrar): ")

while livro_procurado.lower() != "sair":
    livro_encontrado = buscar_livro(livro_procurado, Livros)
    if livro_encontrado:
        print(f'O livro "{livro_encontrado.titulo}" {atual(livro_encontrado)} e {caro(livro_encontrado, Livros)}')
    else:
        print("Livro não encontrado.")
    
    livro_procurado = input("\nDigite o título do livro (ou 'sair' para encerrar): ")
