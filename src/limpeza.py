from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "dados" / "olist_order_reviews_dataset.csv"
SAIDA = RAIZ / "dados" / "reviews_limpos.csv"

df = pd.read_csv(ENTRADA)
print("Linhas iniciais:", len(df))

# 1. Entender os duplicados antes de apagar
print("Linhas totalmente iguais:", df.duplicated().sum())
print("review_id repetido:", df["review_id"].duplicated().sum())
print("review_id + order_id repetido:",
      df.duplicated(subset=["review_id", "order_id"]).sum())

# 2. Uma avaliação = uma opinião (evita contar a mesma opinião duas vezes)
df = df.drop_duplicates(subset="review_id", keep="first")

# 3. Título quase sempre vazio: removemos a coluna
df = df.drop(columns=["review_comment_title"])

# 4. Datas como data de verdade
df["review_creation_date"] = pd.to_datetime(df["review_creation_date"])
df["review_answer_timestamp"] = pd.to_datetime(df["review_answer_timestamp"])

# 5. Texto: tira espaços sobrando e trata vazio como ausente
df["review_comment_message"] = (
    df["review_comment_message"]
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .replace("", pd.NA)
)

# 6. Marca quem tem comentário
df["tem_comentario"] = df["review_comment_message"].notna()

print("\nLinhas finais:", len(df))
print("Com comentário:", df["tem_comentario"].sum())
print(df.dtypes)

df.to_csv(SAIDA, index=False)
print("\nSalvo em:", SAIDA)