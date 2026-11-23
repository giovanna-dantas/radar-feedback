from pathlib import Path
import pandas as pd  # pyright: ignore[reportMissingModuleSource]

# Caminho relativo à raiz do projeto (funciona de qualquer pasta)
RAIZ = Path(__file__).resolve().parent.parent
ARQUIVO = RAIZ / "dados" / "olist_order_reviews_dataset.csv"

dados = pd.read_csv(ARQUIVO)

print("DIMENSÕES:", dados.shape)
print("\nCOLUNAS:", list(dados.columns))
print("\nPRIMEIRAS LINHAS:")
print(dados.head())

print("\nINFO:")
dados.info()

print("\nVALORES AUSENTES:")
print(dados.isna().sum())

print("\nDISTRIBUIÇÃO DAS NOTAS:")
print(dados["review_score"].value_counts().sort_index())

print("\nREVIEW_ID DUPLICADOS:", dados["review_id"].duplicated().sum())