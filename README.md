# Radar Feedback

Projeto de análise de avaliações de clientes para descobrir **por que as pessoas ficam insatisfeitas** e como isso muda ao longo do tempo.

## Pergunta guia

> Quais são os principais motivos de insatisfação nos clientes da Olist, e como eles evoluem ao longo do tempo?

## Por que este projeto existe

A ideia nasceu de um problema real: participei das vendas de produtos do centro acadêmico do meu curso e vi como é difícil transformar o feedback dos clientes em ações. Este projeto é a versão em dados desse problema, aplicada a uma base pública de e-commerce.

## Tecnologias

- **Python** e **Pandas** para limpeza e análise
- **Kaggle**: base de dados [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **Gemini API** para apoiar a identificação de temas nos comentários
- **VS Code** como ambiente de desenvolvimento

## Sobre os dados

O dataset da Olist reúne avaliações reais de pedidos feitos em lojas brasileiras. Este projeto usa o arquivo `olist_order_reviews_dataset.csv`.

| Informação                         | Valor  |
| ---------------------------------- | ------ |
| Avaliações originais               | 99.224 |
| Avaliações após a limpeza          | 98.410 |
| Avaliações com comentário em texto | 40.641 |

## Decisões de limpeza

- **Duplicados:** 814 `review_id` apareciam repetidos, ligados a pedidos diferentes (não eram linhas idênticas). Mantive uma linha por `review_id` para que a mesma opinião não pese duas vezes na análise de texto.
- **Título do comentário:** removido, pois cerca de 88% estava vazio.
- **Datas:** convertidas de texto para data.
- **Texto:** espaços extras removidos e comentários vazios tratados como ausentes.
- **Nova coluna `tem_comentario`:** indica quais avaliações têm texto para análise.

## Estrutura do projeto

```
radar-feedbacks/
├── dados/          # CSVs (não versionados, baixe no Kaggle)
├── src/
│   ├── main.py     # exploração inicial da base
│   └── limpeza.py  # limpeza e geração de reviews_limpos.csv
├── .env            # chaves de API (não versionado)
├── .gitignore
└── README.md
```

## Como rodar

1. Clone o repositório e crie o ambiente virtual:

```bash
python -m venv .venv
source .venv/Scripts/activate   # Git Bash no Windows
pip install pandas
```

2. Baixe o dataset no Kaggle e coloque `olist_order_reviews_dataset.csv` dentro da pasta `dados/`.
3. Rode a exploração e a limpeza:

```bash
python src/main.py
python src/limpeza.py
```

## Status

- [x] Estrutura do projeto
- [x] Exploração da base
- [x] Limpeza dos dados
- [ ] Análise exploratória (notas, volume e tempo)
- [ ] Identificação dos motivos de insatisfação nas notas 1 e 2
- [ ] Evolução dos motivos ao longo do tempo
- [ ] Gráficos e conclusões

## Resultados

_Em construção._

## Aprendizados

Este projeto faz parte da minha jornada de estudo em análise de dados. Vou registrar aqui o que aprendi em cada etapa.

