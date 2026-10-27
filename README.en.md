<p align="center"><img src="https://dodysalim.github.io/assets/project-covers/conversaai.webp" alt="ConversaAI" width="100%"></p>

<h1 align="center">ConversaAI</h1>

<p align="center"><b>Bilingual (ES/PT) NLP that classifies sentiment, intent and churn risk in customer-support conversations.</b></p>

<p align="center"><img src="https://img.shields.io/badge/No_Country_·_Team_40_·_April_2026-75E6CE?style=for-the-badge&labelColor=0b1222" alt="No Country · Team 40 · April 2026"></p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" alt="PyTorch"> <img src="https://img.shields.io/badge/Transformers-FFD21E?style=flat-square&logo=huggingface&logoColor=black" alt="Transformers"> <img src="https://img.shields.io/badge/Hugging_Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black" alt="Hugging Face"> <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"> <img src="https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white" alt="Plotly"> <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker">
</p>

<p align="center"><a href="https://dodysalim.github.io/"><b>🌐 Portfolio</b></a> · <a href="https://rosela-conversaai-dashboard.hf.space"><b>🚀 Live demo (HF Space)</b></a> · <a href="https://nocountry.tech/showcase/simulacion-laboral-abril-2026/equipo-40-data-science"><b>🏆 No Country Showcase</b></a> · <a href="README.md"><b>🇪🇸 Versión en español</b></a></p>

---

## 📌 At a glance

| | |
| --- | --- |
| **🎯 Problem** | Prioritize support conversations by understanding what each customer feels and needs. |
| **🛠️ Solution** | Two fine-tuned XLM-R models (3 sentiment classes, 9 intents) plus a heuristic churn score. |
| **📈 Published results** | ~92.2% sentiment accuracy and ~99.6% intent F1 on the team's evaluation sets. |
| **🧪 Quality** | 12 offline tests; the dashboard runs without GPU using a swappable rule-based engine. |
| **👤 My role** | Data Scientist in a 4-person team. |

## 🏗️ Architecture

```mermaid
flowchart LR
    MSG[Mensaje ES/PT] --> ENG{AnalysisEngine}
    ENG -->|Strategy| XLMR[TransformerEngine<br/>XLM-R fine-tuneado]
    ENG -->|Strategy| RULES[RuleBasedEngine<br/>offline]
    XLMR --> S[Sentimiento<br/>3 clases]
    XLMR --> I[Intención<br/>9 clases]
    RULES --> S
    RULES --> I
    S --> CH[ChurnScorer<br/>heurístico]
    I --> CH
    CH --> AN[analysis<br/>funciones puras]
    AN --> UI[Dashboard Streamlit<br/>Dashboard · Explorar · Acciones]
```

## 🚀 How to run

```bash
pip install -r requirements-dashboard.txt
streamlit run dashboard-streamlit/dashboard_app.py
pip install pytest pandas && python -m pytest proyecto/tests -q
```

## ⚖️ Scope

Churn risk is a heuristic score, not a calibrated probability.

## 👥 Team

Team: Rosa Isela González Díaz · Jefferson Mangier · Dody Dueñas Remache · Geyson David. Collective authorship is preserved.

---

<p align="center">
<b>Dody Dueñas Remache</b> · Data Analyst / Data Scientist · Guayaquil, Ecuador (remote LATAM)<br>
<a href="https://dodysalim.github.io/">Portfolio</a> · <a href="https://github.com/dodysalim">GitHub</a> · <a href="https://www.linkedin.com/in/dody-duenas/">LinkedIn</a> · <a href="mailto:dodydurema67@gmail.com">dodydurema67@gmail.com</a>
</p>
