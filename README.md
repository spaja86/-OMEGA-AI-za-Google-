# OMEGA AI za Google 🚀♾️

> **"Omega AI" koji unapređuje i evolvuira Google ka beskonačnosti."**
> — [OMEGA AI ChatGPT Conversation](https://chatgpt.com/c/686787a3-1168-8006-8d37-418e3e220e69)

---

## 📖 Opis / Description

**OMEGA AI** je napredni AI sistem dizajniran da kontinuirano unapređuje i evolvira Google pretragu ka beskonačnosti. Sistem koristi generativnu AI za poboljšanje rezultata pretrage, semantičko razumijevanje upita i evolutivno učenje koje se poboljšava sa svakim novim upitom.

**OMEGA AI** is an advanced AI system designed to continuously improve and evolve Google search towards infinity. The system uses generative AI to enhance search results, provide semantic query understanding, and apply evolutionary learning that improves with every new query.

---

## ✨ Karakteristike / Features

- 🔍 **Google Search Enhancement** — Semantičko poboljšanje rezultata pretrage
- 🧠 **AI Query Expansion** — Automatsko proširivanje upita za bolje rezultate
- ♾️ **Evolutionary Loop** — Sistem koji evolvira i uči iz svakog upita
- 📊 **Score & Rank** — AI bodovanje i rangiranje rezultata
- 🔁 **Feedback Integration** — Integracija povratnih informacija za evoluciju
- 🌐 **Multi-source Fusion** — Spajanje rezultata iz više izvora
- 📈 **Performance Tracking** — Praćenje i mjerenje napretka evolucije

---

## 🏗️ Struktura Projekta / Project Structure

```
omega_ai/
├── __init__.py          # Inicijalizacija paketa
├── config.py            # Konfiguracija sustava
├── core.py              # Glavni OMEGA AI motor
├── search_enhancer.py   # Google Search poboljšivač
├── evolution.py         # Evolucijski AI sistem
├── query_expander.py    # Proširivač upita
├── result_ranker.py     # AI rangiranje rezultata
└── tests/
    ├── __init__.py
    ├── test_core.py
    ├── test_search_enhancer.py
    └── test_evolution.py
main.py                  # Ulazna točka
requirements.txt         # Zavisnosti
```

---

## 🚀 Instalacija / Installation

```bash
# 1. Kloniraj repozitorij
git clone https://github.com/spaja86/-OMEGA-AI-za-Google-.git
cd -OMEGA-AI-za-Google-

# 2. Instaliraj zavisnosti
pip install -r requirements.txt

# 3. Postavi API ključeve (opciono za puni rad)
export GOOGLE_API_KEY="your_google_api_key"
export GOOGLE_CSE_ID="your_custom_search_engine_id"
export OPENAI_API_KEY="your_openai_api_key"   # or any OpenAI-compatible key
```

---

## 💡 Upotreba / Usage

```bash
# Interaktivni mod
python main.py

# Jednostruki upit
python main.py --query "kvantno računarstvo" --evolve

# Prikaz statistike evolucije
python main.py --stats

# Resetovanje memorije evolucije
python main.py --reset
```

### Python API

```python
from omega_ai import OmegaAI

# Inicijalizacija
omega = OmegaAI()

# Poboljšana pretraga
results = omega.search("kvantno računarstvo buducnost")

# Svaki rezultat je obogaćen AI analizom
for r in results:
    print(r.title)
    print(r.ai_summary)
    print(r.relevance_score)

# Evolucija — ručno pokretanje jednog ciklusa
omega.evolution.run_cycle()

# Statistika
stats = omega.evolution.get_stats()
print(f"Generacija: {stats['generation']}")
print(f"Ukupno upita: {stats['total_queries']}")
print(f"Avg relevance: {stats['avg_relevance_score']:.2f}")
```

---

## 🧬 Evolucijski Sistem / Evolutionary System

OMEGA AI koristi evolucijski pristup učenja:

1. **Inicijalizacija (Gen 0)** — Bazni pretraživač sa default parametrima
2. **Evaluacija** — Svaki upit se boduje po relevantnosti i korisnosti
3. **Selekcija** — Najuspješnije strategije se zadržavaju
4. **Mutacija** — Parametri se mutiraju za eksperimentisanje
5. **Reprodukcija** — Uspješne strategije se kombiniraju
6. **Beskonačna Evolucija** — Proces se nikad ne zaustavlja → ♾️

---

## 🌐 OMEGA AI Referenca / Reference

Originalni konceptualni razgovor: [ChatGPT OMEGA AI](https://chatgpt.com/c/686787a3-1168-8006-8d37-418e3e220e69)

---

## 📄 Licenca / Licence

MIT License — slobodna upotreba za evoluciju ka beskonačnosti.
