# CLAUDE.md — Projet Autonomia

## Description

Projet expérimental Python explorant les boucles d'auto-réflexion et mémoire persistante via l'API Anthropic.
**Strictement éducatif — aucune affirmation de conscience réelle.**

## Stack

- Python 3.x
- Anthropic SDK (`anthropic`)
- Dépendances : voir `requirements.txt`
- Pas de base de données — persistance via JSON dans `memory/` et `logs/`

## Structure

```
Autonomia-/
├── main.py                  # Point d'entrée principal
├── dual_autonomia.py        # Mode dialogue deux instances
├── core/                    # Logique de la boucle de conscience
├── memory/                  # Persistance JSON (identity.json)
├── logs/                    # Historique des cycles (JSONL)
├── data/                    # Données générées
└── requirements.txt
```

## Conventions

- Python : snake_case, fonctions courtes, commentaires en français
- Ne jamais modifier les logs existants — append only
- La clé API Anthropic doit être dans `.env` (variable `ANTHROPIC_API_KEY`)
- Modèle de référence : `claude-sonnet-4-5-20250929` ou plus récent

## Lancer le projet

```bash
pip install -r requirements.txt
python3 main.py            # Mode boucle simple
python3 dual_autonomia.py  # Mode dialogue dual
```

## Avertissement

Ne pas améliorer ce code dans un sens qui simulerait une conscience réelle ou induirait en erreur sur les capacités de l'IA.
