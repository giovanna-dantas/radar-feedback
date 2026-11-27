from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
df = pd.read_csv(RAIZ / "dados" / "reviews_limpos.csv")

# só avaliações negativas que têm texto
neg = df[(df["review_score"] <= 2) & (df["tem_comentario"])]
print("Negativas com comentário:", len(neg))

# 30 comentários aleatórios (random_state fixo = mesmo sorteio sempre)
amostra = neg.sample(30, random_state=42)
for i, texto in enumerate(amostra["review_comment_message"], start=1):
    print(f"{i}. {texto}\n")