from __future__ import annotations

from dataclasses import dataclass

ORIGEM_CURADORIA = "curadoria"
ORIGEM_REGRESSAO = "regressao"


@dataclass(frozen=True)
class CasoGolden:
    """Entidade do Golden Dataset: par (pergunta, resposta de referência)
    validado manualmente por um humano (RN05), usado como baseline de avaliação."""

    id: str
    pergunta: str
    resposta_referencia: str
    tribunal: str
    validado_por: str
    data_validacao: str
    contexto_esperado: str | None = None
    origem: str = ORIGEM_CURADORIA
