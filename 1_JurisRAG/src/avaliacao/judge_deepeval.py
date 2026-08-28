from __future__ import annotations

import os

from .metricas import CalculadorMetricas, CasoAvaliado

MODELO_JUDGE_PADRAO = "openai/gpt-4o-mini"


class VariavelAmbienteFaltandoError(RuntimeError):
    pass


def _variavel_obrigatoria(nome: str) -> str:
    valor = os.environ.get(nome)
    if not valor:
        raise VariavelAmbienteFaltandoError(
            f"variável de ambiente {nome} não definida — configure no .env (ver .env.example)"
        )
    return valor


def criar_calculador_deepeval(modelo: str | None = None) -> CalculadorMetricas:
    """Cria o Calculador de Métricas real via DeepEval (RF02), usando o
    OpenRouter (mesmo provedor do modelo de geração de F4) como Judge Model —
    RNF02: reaproveita a credencial `OPENROUTER_API_KEY` já configurada em vez
    de exigir uma chave de judge separada (o DeepEval tem suporte nativo a
    `OpenRouterModel`, compatível com a API da OpenAI). Usa `modelo` (ou
    `AVALIACAO_JUDGE_MODEL` do ambiente, com um default barato) para as 4
    Métricas mínimas de RN01. Falha rápido aqui, na criação do calculador, se
    `OPENROUTER_API_KEY` não estiver configurada.
    """
    from deepeval.metrics import (
        AnswerRelevancyMetric,
        ContextualPrecisionMetric,
        ContextualRecallMetric,
        FaithfulnessMetric,
    )
    from deepeval.models.llms.openrouter_model import OpenRouterModel
    from deepeval.test_case import LLMTestCase

    api_key = _variavel_obrigatoria("OPENROUTER_API_KEY")
    nome_modelo = modelo or os.environ.get("AVALIACAO_JUDGE_MODEL", MODELO_JUDGE_PADRAO)

    def _calcular(caso_avaliado: CasoAvaliado) -> dict[str, float]:
        # `executar_avaliacao` roda os Casos Golden concorrentemente (RNF01) e
        # cada `metric.measure()` do DeepEval gerencia seu próprio event loop
        # assíncrono internamente — compartilhar uma única instância de
        # `OpenRouterModel` (e seu cliente HTTP assíncrono) entre threads com
        # loops diferentes corrompe esse estado no Windows (`ProactorEventLoop`).
        # Uma instância nova por chamada evita isso; o custo é desprezível
        # perto da latência de rede do Judge Model.
        judge = OpenRouterModel(model=nome_modelo, api_key=api_key)
        contexto = [chunk.texto for chunk in caso_avaliado.resposta.contexto.chunks]
        caso_teste = LLMTestCase(
            input=caso_avaliado.caso.pergunta,
            actual_output=caso_avaliado.resposta.texto_resposta,
            expected_output=caso_avaliado.caso.resposta_referencia,
            # `list[str]` é aceito em runtime, mas o stub do DeepEval declara o
            # parâmetro como invariante em `list[str | RetrievedContextData]`.
            retrieval_context=contexto,  # type: ignore[arg-type]
        )
        # `async_mode=False`: por padrão, cada métrica cria seu próprio event
        # loop assíncrono dentro de `.measure()` — com `executar_avaliacao` já
        # paralelizando por thread entre Casos Golden (RNF01), múltiplos loops
        # concorrentes por thread corrompem o `ProactorEventLoop` no Windows.
        # Rodar cada métrica de forma síncrona evita o problema; a paralelização
        # entre casos (não intra-métrica) já é suficiente para o orçamento.
        metricas = {
            "faithfulness": FaithfulnessMetric(model=judge, async_mode=False),
            "context_precision": ContextualPrecisionMetric(model=judge, async_mode=False),
            "context_recall": ContextualRecallMetric(model=judge, async_mode=False),
            "answer_relevancy": AnswerRelevancyMetric(model=judge, async_mode=False),
        }
        resultado: dict[str, float] = {}
        for nome, metrica in metricas.items():
            metrica.measure(caso_teste)
            resultado[nome] = metrica.score if metrica.score is not None else 0.0
        return resultado

    return _calcular
