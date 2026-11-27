from pathlib import Path
import pandas as pd
import matplotlib
# "Agg" = backend que só GERA ARQUIVOS, sem abrir janela.
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parent.parent
GRAFICOS = RAIZ / "graficos"
# exist_ok=True: se a pasta já existir, não dá erro
GRAFICOS.mkdir(exist_ok=True)


# parse_dates converte essas colunas de texto para datetime na leitura.
# Sem isso, o pandas trata data como texto e não dá para agrupar por mês.
df = pd.read_csv(
    RAIZ / "dados" / "reviews_limpos.csv",
    parse_dates=["review_creation_date", "review_answer_timestamp"],
)

# 1. Como as notas se distribuem?
# value_counts() conta quantas vezes cada nota aparece.
# sort_index() ordena pela nota (1 a 5) em vez de pela contagem.
contagem = df["review_score"].value_counts().sort_index()

# Dividir pelo total dá a proporção; * 100 vira percentual.
# Percentual é melhor que contagem para comparar partes de um todo.
percentual = (contagem / len(df) * 100).round(1)
print("Percentual por nota:")
print(percentual)

# Gráfico de barras: uma barra por nota
contagem.plot(kind="bar")
plt.title("Distribuição das Notas")
plt.xlabel("Nota")
plt.ylabel("Qtde de Avaliações")
plt.tight_layout()                                  # evita cortar os rótulos
plt.savefig(GRAFICOS / "01_distribuicao_notas.png")
# plt.close() limpa a figura; sem ele, o próximo gráfico seria
# desenhado em cima deste.
plt.close()
print("gráfico 1 salvo")

# LEITURA: ~58% são nota 5 e ~15% são notas 1 e 2.

# 2. Como o volume e a insatisfação mudam por mês?
# to_period("M") troca cada data pelo mês dela (2017-03-14 -> 2017-03),
# criando a chave para agrupar.
df["mes"] = df["review_creation_date"].dt.to_period("M")

# groupby("mes") junta as avaliações de cada mês.
# agg() calcula várias métricas de uma vez, no formato nome=(coluna, função).
por_mes = df.groupby("mes").agg(
    total=("review_id", "count"),            # quantas avaliações no mês
    nota_media=("review_score", "mean"),     # nota média do mês
    # (s <= 2) transforma cada nota em True/False. mean() de True/False é a
    # PROPORÇÃO de True (ex.: 0.15). O "* 100" é que converte em percentual.
    pct_negativas=("review_score", lambda s: (s <= 2).mean() * 100),
)

print("\nPor mês:")
print(por_mes.round(2))

# Gráfico 2: volume por mês
por_mes["total"].plot(kind="line", marker="o")
plt.title("Avaliações por mês")
plt.ylabel("Quantidade")
plt.tight_layout()
plt.savefig(GRAFICOS / "02_volume_mes.png")
plt.close()
print("gráfico 2 salvo")

# Gráfico 3: % de negativas por mês
por_mes["pct_negativas"].plot(kind="line", marker="o")
plt.title("% de avaliações negativas (notas 1 e 2) por mês")
plt.ylabel("%")
plt.tight_layout()
plt.savefig(GRAFICOS / "03_pct_negativas_mes.png")
plt.close()
print("gráfico 3 salvo")

# 3. Quem escreve comentários?
# tem_comentario é True/False (criada no limpeza.py). A média de True/False
# por nota é a proporção de quem comentou em cada nota.
taxa_comentario = (df.groupby("review_score")["tem_comentario"].mean() * 100).round(1)
print("\n% QUE COMENTA, POR NOTA:")
print(taxa_comentario)

# LEITURA: ~77% de quem deu nota 1 comenta, contra ~36% de quem deu nota 5.
# Insatisfeito escreve mais, então o texto está concentrado onde queremos olhar.