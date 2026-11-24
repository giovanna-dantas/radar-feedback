from pathlib import Path
import unicodedata
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parent.parent
GRAFICOS = RAIZ / "graficos"
GRAFICOS.mkdir(exist_ok=True)

df = pd.read_csv(
    RAIZ / "dados" / "reviews_limpos.csv",
    parse_dates=["review_creation_date"],  # só preciso da data da avaliação aqui
)

# 1. Filtrar: só negativas COM comentário 
neg = df[(df["review_score"] <= 2) & (df["tem_comentario"])].copy()
print("Negativas com comentário:", len(neg))

# 2. Normalizar o texto 
# Clientes escrevem "não", "nao", "NÃO"... Se eu não padronizar, preciso
# prever todas as variações. Aqui: tudo minúsculo e sem acento.
def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in texto if not unicodedata.combining(c))

neg["texto"] = neg["review_comment_message"].map(normalizar)

# 3. Dicionário: tema -> expressão de busca (regex) 
# "|" significa "ou". (?:...) agrupa sem capturar. \d+ = um ou mais dígitos.
# O texto já está sem acento, então escrevo as palavras sem acento também.
TEMAS = {
    "nao_entregue": r"nao (?:foi )?(?:recebi|recebemos|chegou|chegaram|entreg|aguardando|onde esta|cade(?:o )?meu)|"
                    r"nunca (?:recebi|chegou)|ainda nao (?:recebi|chegou)|"
                    r"nao me entreg|nao veio",
    "atraso":       r"prazo|atras|demor|previsao|\d+ dias",
    "anuncio_divergente": r"diferente|propaganda enganosa|enganos|"
                          r"nao (?:e|era) o que|foto|anunci|descricao|"
                          r"especificad|exposto",
    "produto_errado": r"errad|trocaram|veio outro|outro produto|nao pedi",
    "entrega_incompleta": r"falta(?:m)? (?:1|um|uma|dois|o)|faltou|faltando|"
                          r"pela metade|cade (?:o|a) outr|somente (?:recebi|\d|um|uma)|apenas(?:\d|um|uma|dois|tres|quatro)|chegou (?:um|1)\b|chegaram (?:apenas|somente|so)|nao foi enviado|recebi (?:so|somente|apenas)"
                          r"so (?:chegou|veio|foi enviado)|apenas (?:um|1)|"
                          r"um dos (?:produtos|itens)|incompleto",
    "sem_retorno":  r"sem (?:resposta|retorno|satisfacao|contato)|"
                    r"nenhum(?:a)? (?:retorno|resposta|satisfacao|contato|posicao)|"
                    r"nao (?:tive|obtive|deram|dao) (?:retorno|resposta|satisfacao)|"
                    r"ninguem (?:responde|me)|atendimento|nao atendem",
    "defeito_qualidade": r"defeito|quebr|danific|nao funcion|nao liga|estrag|"
                         r"rasg|amass|avaria|qualidade|falsific|falso|nao (?:e|era) original|usad[oa]|pessim|ruim",
    "reembolso_cancelamento": r"reembols|estorn|dinheiro|devol|cancel|cobran|cobrad",
}

# 4. Criar uma coluna True/False para cada tema 
for tema, padrao in TEMAS.items():
    neg[tema] = neg["texto"].str.contains(padrao, regex=True)

temas = list(TEMAS)

# 5. Quais temas são mais frequentes? 
# .sum() de True/False = quantos comentários têm o tema.
# Dividindo pelo total de negativas, vira percentual.
percentual = (neg[temas].mean() * 100).round(1).sort_values(ascending=False)
print("\n% DAS NEGATIVAS QUE MENCIONAM CADA TEMA:")
print(percentual)

percentual.sort_values().plot(kind="barh")
plt.title("Motivos de insatisfação (notas 1 e 2 com comentário)")
plt.xlabel("% dos comentários (um comentário pode ter vários temas)")
plt.tight_layout()
plt.savefig(GRAFICOS / "04_motivos.png")
plt.close()
print("gráfico 4 salvo")

#  6. Qual a cobertura? E o que ficou de fora? 
neg["n_temas"] = neg[temas].sum(axis=1)  # soma de colunas True/False por linha
sem_tema = neg[neg["n_temas"] == 0]
print(f"\nSem nenhum tema: {len(sem_tema)} de {len(neg)} "
      f"({len(sem_tema) / len(neg) * 100:.1f}%)")
print("Média de temas por comentário:", round(neg["n_temas"].mean(), 2))

print("\nEXEMPLOS SEM TEMA (leia e pense: que palavra eu esqueci?):")
for i, t in enumerate(sem_tema["review_comment_message"].sample(15, random_state=1), 1):
    print(f"{i}. {t}\n")

# 7. Evolução no tempo
neg["mes"] = neg["review_creation_date"].dt.to_period("M")
neg = neg[neg["mes"] >= "2017-01"]   # antes disso há poucos dados (ruído)

por_mes = neg.groupby("mes")[temas].mean() * 100
por_mes["n_comentarios"] = neg.groupby("mes").size()
print("\nTEMAS POR MÊS (%):")
print(por_mes.round(1))

# Comparar os meses de pico com a média geral
media_geral = neg[temas].mean() * 100
picos = por_mes.loc[[pd.Period("2017-12"), pd.Period("2018-03")], temas]
picos.loc["media_geral"] = media_geral
print("\nPICOS vs MÉDIA GERAL (%):")
print(picos.round(1))

# Gráfico: só os 4 temas mais frequentes, para não poluir
top4 = percentual.head(4).index
por_mes[top4].plot(marker="o")
plt.title("Evolução dos 4 principais motivos (% das negativas do mês)")
plt.ylabel("%")
plt.tight_layout()
plt.savefig(GRAFICOS / "05_motivos_mes.png")
plt.close()
print("gráfico 5 salvo")

neg.drop(columns=["texto"]).to_csv(
    RAIZ / "dados" / "negativas_classificadas.csv", index=False
)
print("CSV salvo")