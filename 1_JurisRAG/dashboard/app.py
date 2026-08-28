from __future__ import annotations

import os
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from avaliacao.dominio import THRESHOLDS_PADRAO
from avaliacao.historico_execucoes import carregar_historico
from dashboard.series_temporal import calcular_variacoes, montar_series_temporais

CAMINHO_HISTORICO_PADRAO = Path("data/avaliacoes/historico_execucoes.jsonl")


def _caminho_historico() -> Path:
    """Lê `AVALIACAO_HISTORICO_PATH` para permitir apontar para outro
    histórico (testes, ambientes) sem mudar o código — mesmo padrão de F4/F6."""
    return Path(os.environ.get("AVALIACAO_HISTORICO_PATH", str(CAMINHO_HISTORICO_PADRAO)))


st.set_page_config(page_title="JurisRAG — Avaliação", layout="wide")
st.title("JurisRAG — Evolução das Métricas de Avaliação")
st.caption(
    "Lê apenas o histórico já persistido por F6 (RNF03) — nenhuma métrica é "
    "recalculada aqui."
)

caminho_historico = _caminho_historico()
historico = carregar_historico(caminho_historico)

if not historico:
    st.info(
        f"Nenhuma Execução de Avaliação encontrada em `{caminho_historico}`. "
        "Rode o script de avaliação de F6 (`avaliacao.executar_avaliacao_cli`) "
        "para gerar a primeira."
    )
    st.stop()

st.caption(f"{len(historico)} Execução(ões) de Avaliação carregada(s).")

series = montar_series_temporais(historico, THRESHOLDS_PADRAO)

for nome_metrica in sorted(series):
    serie = series[nome_metrica]
    st.subheader(nome_metrica)

    eixo_x = [f"{ponto.commit_sha[:7]} · {ponto.timestamp[:10]}" for ponto in serie.pontos]
    valores = [ponto.valor for ponto in serie.pontos]

    figura = go.Figure()
    figura.add_trace(go.Scatter(x=eixo_x, y=valores, mode="lines+markers", name=nome_metrica))
    if serie.threshold is not None:
        figura.add_hline(
            y=serie.threshold,
            line_dash="dash",
            line_color="red",
            annotation_text=f"threshold {serie.threshold}",
        )
    figura.update_layout(
        yaxis_range=[0, 1], xaxis_title="Execução (commit · data)", yaxis_title="valor"
    )
    st.plotly_chart(figura, use_container_width=True)

    variacoes = calcular_variacoes(serie)
    if variacoes:
        ultima = variacoes[-1]
        st.metric(
            label="Última variação",
            value=f"{ultima.valor_atual:.3f}",
            delta=f"{ultima.delta:+.3f}",
        )
