import pandas as pd
import json
from unidecode import unidecode
import re

# Ler o JSON gerado pelo Scrapy
with open("arros-preco-giassi.json", "r", encoding='utf-8') as file:
    data = json.load(file)

# Criar DataFrame diretamente (não precisa de normalize complexo pois a estrutura é plana)
df = pd.DataFrame(data)

print(f"Total de produtos coletados: {len(df)}")

# Limpar e normalizar dados
df['nome_limpo'] = df['nome'].apply(lambda x: unidecode(str(x)).strip() if x else '')
df['marca'] = df['marca'].apply(lambda x: unidecode(str(x)).strip() if x else 'Não informada')

# Extrair peso numérico para análise (converter "5kg" para 5.0)
def extrair_peso_numerico(peso_str):
    if not peso_str:
        return None
    match = re.search(r'(\d+(?:[,.]\d+)?)', str(peso_str).replace(',', '.'))
    return float(match.group(1)) if match else None

df['peso_numerico'] = df['peso'].apply(extrair_peso_numerico)

# Converter preços para float (remover R$ e trocar vírgula por ponto)
def limpar_preco(preco_str):
    if not preco_str or preco_str == 'None':
        return None
    # Remove R$, espaços, e troca vírgula por ponto
    limpo = re.sub(r'[R$\s]', '', str(preco_str)).replace('.', '').replace(',', '.')
    try:
        return float(limpo)
    except:
        return None

df['preco_num'] = df['preco'].apply(limpar_preco)
df['preco_de_num'] = df['preco_de'].apply(limpar_preco)

# Calcular desconto quando houver preço de e preço por
df['desconto_percentual'] = ((df['preco_de_num'] - df['preco_num']) / df['preco_de_num'] * 100).round(2)
df['economia'] = (df['preco_de_num'] - df['preco_num']).round(2)

# Calcular preço por kg para comparação justa
df['preco_por_kg'] = (df['preco_num'] / df['peso_numerico']).round(2)

print("\n--- 📊 ANÁLISE DE PREÇOS DE ARROZ - GISSI ---\n")

# 1. Produtos que precisam de login (sem preço)
sem_preco = df[df['precisa_login_para_preco'] == True]
print(f"⚠️  Produtos sem preço visível (precisam de login): {len(sem_preco)}")

# 2. Ranking por tipo de arroz
print("\n--- 🌾 Quantidade por Tipo de Arroz ---")
tipo_counts = df['tipo_arroz'].value_counts()
print(tipo_counts)

# 3. Análise de preços por tipo (apenas produtos com preço)
df_com_preco = df[df['preco_num'].notna()]

if not df_com_preco.empty:
    print("\n--- 💰 Estatísticas de Preço por Tipo ---")
    stats_preco = df_com_preco.groupby('tipo_arroz')['preco_num'].agg(['count', 'mean', 'min', 'max']).round(2)
    stats_preco.columns = ['Qtd', 'Média R$', 'Mínimo R$', 'Máximo R$']
    print(stats_preco)
    
    print("\n--- ⚖️  Preço por Kg (para comparação justa) ---")
    stats_kg = df_com_preco[df_com_preco['preco_por_kg'].notna()].groupby('tipo_arroz')['preco_por_kg'].agg(['mean', 'min']).round(2)
    stats_kg.columns = ['Média R$/kg', 'Melhor R$/kg']
    print(stats_kg.sort_values('Média R$/kg'))
    
    # 4. Top 10 mais baratos por kg
    print("\n--- 🏆 TOP 10 - Melhor Custo-Benefício (R$/kg) ---")
    top_custo = df_com_preco[df_com_preco['preco_por_kg'].notna()].nsmallest(10, 'preco_por_kg')
    print(top_custo[['nome', 'marca', 'peso', 'preco', 'preco_por_kg']].to_string())
    
    # 5. Produtos em promoção
    promocoes = df_com_preco[df_com_preco['desconto_percentual'] > 0]
    if not promocoes.empty:
        print(f"\n--- 🔥 Produtos em Promoção ({len(promocoes)} itens) ---")
        print(promocoes[['nome', 'preco_de', 'preco', 'desconto_percentual']].sort_values('desconto_percentual', ascending=False).to_string())
    
    # 6. Análise por marca
    print("\n--- 🏭 Média de Preço por Marca ---")
    marca_stats = df_com_preco.groupby('marca')['preco_num'].mean().round(2).sort_values()
    print(marca_stats)

# 7. Exportar resultados para CSV
df.to_csv('analise_arroz_giassi.csv', index=False, encoding='utf-8-sig')
print("\n✅ Arquivo 'analise_arroz_giassi.csv' exportado com sucesso!")

# 8. Filtros específicos (exemplo: arroz parboilizado até R$ 20)
print("\n--- 🔍 EXEMPLO DE FILTRO: Arroz Parboilizado até R$ 20 ---")
filtro = df_com_preco[
    (df_com_preco['tipo_arroz'] == 'Parboilizado') & 
    (df_com_preco['preco_num'] <= 20)
]
if not filtro.empty:
    print(filtro[['nome', 'marca', 'peso', 'preco', 'preco_por_kg']].sort_values('preco_num'))
else:
    print("Nenhum produto encontrado com esses critérios.")