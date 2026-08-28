from __future__ import annotations

from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

st.set_page_config(page_title="JurisRAG", layout="wide")

pagina_metricas = st.Page(
    "paginas/metricas.py", title="Métricas de Avaliação", icon="📊", default=True
)
pagina_chat = st.Page("paginas/chat.py", title="Chat", icon="💬")

navegacao = st.navigation([pagina_metricas, pagina_chat])
navegacao.run()
