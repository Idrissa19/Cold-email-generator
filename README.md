# Cold Email Generator

Application Streamlit qui rédige automatiquement un e-mail de candidature spontanée à partir d'une offre d'emploi en ligne. Il suffit de coller l'URL de l'offre : l'application en extrait les postes, puis écrit un e-mail personnalisé qui renvoie vers les projets du portfolio les plus pertinents.

## Fonctionnement

```
URL de l'offre ─▶ scraping (LangChain WebBaseLoader) ─▶ nettoyage du texte
               ─▶ LLM : extraction des postes en JSON (rôle, expérience, compétences, description)
               ─▶ ChromaDB : recherche des projets du portfolio qui correspondent aux compétences
               ─▶ LLM : rédaction de l'e-mail avec les liens les plus pertinents
```

- **LLM** : `openai/gpt-oss-120b` hébergé sur Groq, via `langchain-groq`, avec une température de 0 pour des sorties stables.
- **Extraction structurée** : le premier prompt renvoie un tableau JSON, validé par `JsonOutputParser`.
- **Recherche sémantique** : le portfolio (`app/resource/my_portfolio.csv`) est indexé dans ChromaDB. Les compétences de chaque offre servent de requête pour retrouver les 2 projets les plus proches.
- **Rédaction** : le second prompt impose un e-mail court (moins de 150 mots), concret, sans formules creuses, qui ne mentionne que des informations présentes dans l'offre.

## Structure

| Fichier | Rôle |
|---|---|
| `app/main.py` | Interface Streamlit |
| `app/chains.py` | Prompts et appels au LLM (extraction, rédaction) |
| `app/my_portfolio.py` | Indexation et recherche du portfolio dans ChromaDB |
| `app/utils.py` | Nettoyage du texte scrapé |
| `app/resource/my_portfolio.csv` | Portfolio : technologies et lien de chaque projet |
| `email_generator.ipynb` | Notebook d'exploration qui a servi à construire le pipeline étape par étape |

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Ajoute ta clé [Groq](https://console.groq.com) dans `.env`.

## Lancement

```bash
streamlit run app/main.py
```

Colle l'URL d'une offre d'emploi (par exemple une offre France Travail), puis clique sur **Submit**.

Pour personnaliser les e-mails, remplace les lignes de `app/resource/my_portfolio.csv` par tes propres projets. Supprime ensuite `app/vectorstore/` pour que l'index soit reconstruit.
