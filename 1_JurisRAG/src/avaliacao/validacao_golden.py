from __future__ import annotations

from .dominio import ORIGEM_REGRESSAO, CasoGolden

TAMANHO_MINIMO = 30
TAMANHO_MAXIMO = 50

# RN05: validado_por não pode ficar vazio nem indicar um processo automatizado.
MARCADORES_VALIDACAO_INVALIDOS = {
    "",
    "ia",
    "ai",
    "auto",
    "automatico",
    "automático",
    "llm",
    "gpt",
    "claude",
    "chatgpt",
    "n/a",
    "na",
    "pendente",
}


class CasoGoldenInvalidoError(ValueError):
    pass


def validar_schema(caso: CasoGolden) -> None:
    """RF-5.1 (parte 1): campos obrigatórios preenchidos."""
    campos_obrigatorios = {
        "pergunta": caso.pergunta,
        "resposta_referencia": caso.resposta_referencia,
        "tribunal": caso.tribunal,
        "validado_por": caso.validado_por,
        "data_validacao": caso.data_validacao,
    }
    for nome, valor in campos_obrigatorios.items():
        if not valor.strip():
            raise CasoGoldenInvalidoError(f"{caso.id}: campo obrigatório '{nome}' vazio")


def validar_validador_humano(caso: CasoGolden) -> None:
    """RF-5.1 (parte 2) / RN05: validado_por precisa identificar um revisor humano."""
    if caso.validado_por.strip().lower() in MARCADORES_VALIDACAO_INVALIDOS:
        raise CasoGoldenInvalidoError(
            f"{caso.id}: validado_por={caso.validado_por!r} não identifica um "
            "revisor humano (RN05)"
        )


def validar_tamanho_dataset(casos: list[CasoGolden]) -> None:
    """RF01: o dataset deve conter entre 30 e 50 Casos Golden."""
    if not (TAMANHO_MINIMO <= len(casos) <= TAMANHO_MAXIMO):
        raise CasoGoldenInvalidoError(
            f"Golden Dataset tem {len(casos)} casos; esperado entre "
            f"{TAMANHO_MINIMO} e {TAMANHO_MAXIMO} (RF01)"
        )


def validar_casos_regressao_preservados(
    casos_anteriores: list[CasoGolden], casos_atuais: list[CasoGolden]
) -> None:
    """RN04: Caso de Regressão, uma vez incorporado, nunca é removido."""
    ids_regressao_anteriores = {c.id for c in casos_anteriores if c.origem == ORIGEM_REGRESSAO}
    ids_atuais = {c.id for c in casos_atuais}
    removidos = ids_regressao_anteriores - ids_atuais
    if removidos:
        raise CasoGoldenInvalidoError(
            f"Casos de Regressão removidos do Golden Dataset (RN04, proibido): {sorted(removidos)}"
        )
